import anthropic
from typing import Optional, List, Dict, Any

class ClaudeContextManager:
    def __init__(self, api_key: str, max_context: int = 200000):
        """
        Initialize context manager for Claude API calls.
        
        Args:
            api_key: Your Anthropic API key
            max_context: Maximum context window (200k for Claude)
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.max_context = max_context
        self.buffer = 1000  # Safety buffer
        
        # Approximate token ratios for Claude
        # Claude uses ~1.3 tokens per word on average
        self.chars_per_token = 4  # Rough estimate: 1 token ≈ 4 characters
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for Claude.
        Claude doesn't have public tokenizer, so we estimate.
        """
        # More accurate estimation methods:
        # 1. Character-based (rough)
        char_estimate = len(text) / self.chars_per_token
        
        # 2. Word-based (slightly better)
        word_count = len(text.split())
        word_estimate = word_count * 1.3
        
        # Take the average for better accuracy
        return int((char_estimate + word_estimate) / 2)
    
    def count_tokens_via_api(self, text: str) -> Optional[int]:
        """
        Get exact token count using Claude's API (costs money but accurate).
        """
        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",  # Cheapest model for counting
                max_tokens=1,
                messages=[{"role": "user", "content": text}],
                metadata={"purpose": "token_counting"}
            )
            # Check response usage for input tokens
            if hasattr(response, 'usage'):
                return response.usage.input_tokens
        except Exception as e:
            print(f"Could not count tokens via API: {e}")
        return None
    
    def safe_claude_call(self,
                        messages: List[Dict[str, str]],
                        system_prompt: Optional[str] = None,
                        desired_max_tokens: int = 4096,
                        model: str = "claude-3-5-sonnet-20241022",
                        strategy: str = "truncate") -> Dict[str, Any]:
        """
        Make a safe Claude API call that respects context limits.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: Optional system prompt
            desired_max_tokens: Desired max tokens for response
            model: Claude model to use
            strategy: "truncate", "reduce_max", or "chunk"
        
        Returns:
            Dict with processed input and parameters
        """
        # Estimate total input tokens
        total_text = ""
        if system_prompt:
            total_text += system_prompt + "\n"
        for msg in messages:
            total_text += msg['content'] + "\n"
        
        input_tokens = self.estimate_tokens(total_text)
        available_tokens = self.max_context - self.buffer
        
        # Check if we need to adjust
        if input_tokens + desired_max_tokens > available_tokens:
            if strategy == "reduce_max":
                # Reduce max_tokens to fit
                safe_max_tokens = available_tokens - input_tokens
                if safe_max_tokens < 100:
                    raise ValueError(f"Input too large: ~{input_tokens} tokens")
                
                return {
                    "messages": messages,
                    "system": system_prompt,
                    "max_tokens": safe_max_tokens,
                    "model": model,
                    "estimated_input_tokens": input_tokens,
                    "adjusted": True
                }
            
            elif strategy == "truncate":
                # Truncate messages to fit
                max_input_chars = (available_tokens - desired_max_tokens) * self.chars_per_token
                truncated_messages = self.truncate_messages(messages, max_input_chars)
                
                return {
                    "messages": truncated_messages,
                    "system": system_prompt,
                    "max_tokens": desired_max_tokens,
                    "model": model,
                    "truncated": True
                }
            
            elif strategy == "chunk":
                # Split into conversation chunks
                return self.create_conversation_chunks(
                    messages, system_prompt, desired_max_tokens, model
                )
        
        # No adjustment needed
        return {
            "messages": messages,
            "system": system_prompt,
            "max_tokens": desired_max_tokens,
            "model": model,
            "estimated_input_tokens": input_tokens,
            "adjusted": False
        }
    
    def truncate_messages(self, messages: List[Dict[str, str]], max_chars: int) -> List[Dict[str, str]]:
        """
        Truncate messages to fit within character limit.
        Prioritizes keeping recent messages.
        """
        total_chars = sum(len(msg['content']) for msg in messages)
        
        if total_chars <= max_chars:
            return messages
        
        # Keep most recent messages that fit
        truncated = []
        char_count = 0
        
        for msg in reversed(messages):
            msg_chars = len(msg['content'])
            if char_count + msg_chars <= max_chars:
                truncated.insert(0, msg)
                char_count += msg_chars
            else:
                # Partially include this message if it's the first
                if not truncated:
                    remaining_chars = max_chars - char_count
                    truncated_content = msg['content'][-remaining_chars:]
                    truncated.insert(0, {
                        'role': msg['role'],
                        'content': f"[...truncated...]\n{truncated_content}"
                    })
                break
        
        return truncated
    
    def create_conversation_chunks(self,
                                  messages: List[Dict[str, str]],
                                  system_prompt: Optional[str],
                                  desired_max_tokens: int,
                                  model: str) -> Dict[str, Any]:
        """
        Split conversation into chunks for sequential processing.
        """
        available_for_input = self.max_context - desired_max_tokens - self.buffer
        max_chars_per_chunk = available_for_input * self.chars_per_token
        
        chunks = []
        current_chunk = []
        current_chars = len(system_prompt) if system_prompt else 0
        
        for msg in messages:
            msg_chars = len(msg['content'])
            
            if current_chars + msg_chars > max_chars_per_chunk and current_chunk:
                # Save current chunk and start new one
                chunks.append(current_chunk)
                current_chunk = [msg]
                current_chars = msg_chars
            else:
                current_chunk.append(msg)
                current_chars += msg_chars
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return {
            "chunks": chunks,
            "system": system_prompt,
            "max_tokens": desired_max_tokens,
            "model": model,
            "total_chunks": len(chunks),
            "strategy": "chunk"
        }
    
    def make_api_call(self, params: Dict[str, Any]) -> anthropic.types.Message:
        """
        Actually make the Claude API call with processed parameters.
        """
        if "chunks" in params:
            # Handle chunked processing
            responses = []
            for i, chunk in enumerate(params['chunks']):
                print(f"Processing chunk {i+1}/{params['total_chunks']}")
                response = self.client.messages.create(
                    model=params['model'],
                    max_tokens=params['max_tokens'],
                    messages=chunk,
                    system=params.get('system')
                )
                responses.append(response)
            return responses
        else:
            # Single API call
            return self.client.messages.create(
                model=params['model'],
                max_tokens=params['max_tokens'],
                messages=params['messages'],
                system=params.get('system')
            )


# Example usage for Claude:
def main():
    # Initialize manager
    manager = ClaudeContextManager(api_key="your-api-key-here")
    
    # Example messages
    messages = [
        {"role": "user", "content": "Very long content here..." * 10000},
        {"role": "assistant", "content": "Previous response..."},
        {"role": "user", "content": "Another very long message..." * 10000}
    ]
    
    system_prompt = "You are a helpful assistant."
    
    # Method 1: Reduce max_tokens
    result = manager.safe_claude_call(
        messages=messages,
        system_prompt=system_prompt,
        desired_max_tokens=21333,
        strategy="reduce_max"
    )
    
    if result.get('adjusted'):
        print(f"Adjusted max_tokens to: {result['max_tokens']}")
    
    # Method 2: Truncate messages
    result = manager.safe_claude_call(
        messages=messages,
        system_prompt=system_prompt,
        desired_max_tokens=21333,
        strategy="truncate"
    )
    
    if result.get('truncated'):
        print("Messages were truncated to fit")
    
    # Method 3: Make the actual API call
    try:
        response = manager.make_api_call(result)
        if isinstance(response, list):
            # Multiple responses from chunks
            for r in response:
                print(r.content[0].text)
        else:
            print(response.content[0].text)
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    main()
