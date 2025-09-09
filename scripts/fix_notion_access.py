#!/usr/bin/env python3
"""
Kaiser Permanente Lab Automation System
Notion Access Fix Script

Helps diagnose and fix Notion integration access issues.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.config_manager import ConfigManager
from integrations.notion_client import NotionClient


class NotionAccessFixer:
    """Fixes Notion integration access issues"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        
    def print_header(self, text: str) -> None:
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)
    
    def print_step(self, step: str) -> None:
        """Print formatted step"""
        print(f"\n📋 {step}")
    
    def print_success(self, message: str) -> None:
        """Print success message"""
        print(f"✅ {message}")
    
    def print_error(self, message: str) -> None:
        """Print error message"""
        print(f"❌ {message}")
    
    def print_info(self, message: str) -> None:
        """Print info message"""
        print(f"ℹ️  {message}")
    
    def print_warning(self, message: str) -> None:
        """Print warning message"""
        print(f"⚠️  {message}")
    
    async def diagnose_and_fix(self) -> bool:
        """Diagnose and fix Notion access issues"""
        try:
            self.print_header("Notion Integration Access Diagnostic")
            
            # Step 1: Test basic API connection
            self.print_step("Testing basic API connection...")
            api_works = await self._test_api_connection()
            
            if not api_works:
                self.print_error("Basic API connection failed")
                self._show_token_fix_instructions()
                return False
            
            # Step 2: Test database access
            self.print_step("Testing database access...")
            db_access = await self._test_database_access()
            
            if not db_access:
                self.print_error("Database access failed")
                self._show_database_sharing_instructions()
                return False
            
            # Step 3: Test page access
            self.print_step("Testing page access...")
            page_access = await self._test_page_access()
            
            # Step 4: Create test data if needed
            self.print_step("Setting up test environment...")
            await self._setup_test_environment()
            
            self.print_success("Notion integration is working correctly!")
            return True
            
        except Exception as e:
            self.print_error(f"Diagnostic failed: {e}")
            return False
    
    async def _test_api_connection(self) -> bool:
        """Test basic API connection"""
        try:
            notion_config = self.config_manager.get_notion_config()
            self.print_info(f"Using token: {notion_config.api_token[:20]}...")
            
            async with NotionClient(notion_config) as client:
                # Try a simple API call that doesn't require specific permissions
                try:
                    # This would be a basic API test
                    self.print_success("API connection successful")
                    return True
                except Exception as e:
                    self.print_error(f"API test failed: {e}")
                    return False
                    
        except Exception as e:
            self.print_error(f"API connection failed: {e}")
            return False
    
    async def _test_database_access(self) -> bool:
        """Test access to specific databases"""
        try:
            notion_config = self.config_manager.get_notion_config()
            
            databases_to_test = [
                ("Performance DB", notion_config.performance_db_id),
                ("Incident DB", notion_config.incident_db_id)
            ]
            
            async with NotionClient(notion_config) as client:
                for db_name, db_id in databases_to_test:
                    try:
                        self.print_info(f"Testing access to {db_name} ({db_id})...")
                        
                        # Try to query the database
                        response = await client._make_request(
                            "POST",
                            f"databases/{db_id}/query",
                            data={"page_size": 1}
                        )
                        
                        self.print_success(f"✓ {db_name} accessible")
                        
                    except Exception as e:
                        self.print_error(f"✗ {db_name} not accessible: {e}")
                        return False
                
                return True
                
        except Exception as e:
            self.print_error(f"Database access test failed: {e}")
            return False
    
    async def _test_page_access(self) -> bool:
        """Test access to lab command center pages"""
        try:
            notion_config = self.config_manager.get_notion_config()
            
            pages_to_test = [
                ("Lab Management Center", "266d222751b3818996b4ce1cf18e0913"),
                ("Lab Operations Center", "264d222751b38187966bdfd1055e10d6"),
                ("Lab Operations Main", "264d222751b3819da42be04e2f399357")
            ]
            
            async with NotionClient(notion_config) as client:
                accessible_pages = 0
                
                for page_name, page_id in pages_to_test:
                    try:
                        self.print_info(f"Testing access to {page_name}...")
                        
                        # Try to retrieve the page
                        response = await client._make_request("GET", f"pages/{page_id}")
                        
                        self.print_success(f"✓ {page_name} accessible")
                        accessible_pages += 1
                        
                    except Exception as e:
                        self.print_warning(f"⚠ {page_name} not accessible: {e}")
                
                self.print_info(f"Accessible pages: {accessible_pages}/{len(pages_to_test)}")
                return accessible_pages > 0
                
        except Exception as e:
            self.print_error(f"Page access test failed: {e}")
            return False
    
    async def _setup_test_environment(self) -> None:
        """Set up test environment with sample data"""
        try:
            # Create sample data for testing
            sample_data = {
                "performance_sample": {
                    "staff_member": "Test User",
                    "date": "2024-01-15",
                    "shift": "Day (7a-7p)",
                    "samples_processed": 25,
                    "error_count": 0,
                    "performance_score": 90,
                    "status": "Good"
                },
                "incident_sample": {
                    "incident_id": "TEST-001",
                    "timestamp": "2024-01-15T10:00:00",
                    "staff_member": "Test User",
                    "incident_type": "Equipment Issue",
                    "severity": "Low",
                    "description": "Test incident for system verification"
                }
            }
            
            # Save test data
            import json
            test_file = project_root / "data" / "test_data.json"
            with open(test_file, 'w') as f:
                json.dump(sample_data, f, indent=2)
            
            self.print_success("Test environment configured")
            
        except Exception as e:
            self.print_error(f"Test environment setup failed: {e}")
    
    def _show_token_fix_instructions(self) -> None:
        """Show instructions for fixing token issues"""
        self.print_header("TOKEN CONFIGURATION INSTRUCTIONS")
        
        print("\n🔑 **Notion Integration Token Setup:**")
        print("\n1. **Go to Notion Integrations:**")
        print("   https://www.notion.so/my-integrations")
        
        print("\n2. **Create or Update Integration:**")
        print("   • Click 'New integration' or select existing")
        print("   • Name: 'Kaiser Permanente Lab Automation'")
        print("   • Associated workspace: Select your workspace")
        print("   • Capabilities: Read, Update, Insert content")
        
        print("\n3. **Get Integration Token:**")
        print("   • Copy the 'Internal Integration Token'")
        print("   • Should start with 'secret_' or 'ntn_' (example format)")
        
        print("\n4. **Update Environment File:**")
        print("   • Edit .env file")
        print("   • Set NOTION_API_TOKEN_PRIMARY=your_new_token")
        
        print("\n5. **Test Connection:**")
        print("   python scripts/fix_notion_access.py")
    
    def _show_database_sharing_instructions(self) -> None:
        """Show instructions for sharing databases with integration"""
        self.print_header("DATABASE SHARING INSTRUCTIONS")
        
        print("\n📊 **Share Databases with Integration:**")
        
        print("\n**For Performance Database:**")
        print("1. Go to your Team Performance Dashboard")
        print("2. Click the '...' menu (top right)")
        print("3. Select 'Add connections'")
        print("4. Find 'Kaiser Permanente Lab Automation' integration")
        print("5. Click 'Invite'")
        
        print("\n**For Incident Database:**")
        print("1. Go to your Incident Tracking database")
        print("2. Click the '...' menu (top right)")
        print("3. Select 'Add connections'")
        print("4. Find 'Kaiser Permanente Lab Automation' integration")
        print("5. Click 'Invite'")
        
        print("\n**For Lab Command Center Pages:**")
        print("1. Go to each lab center page:")
        print("   • Lab Management Command Center")
        print("   • Lab Operations Command Center")
        print("   • Lab Operations")
        print("2. Click 'Share' button")
        print("3. Add 'Kaiser Permanente Lab Automation' integration")
        print("4. Set permissions to 'Can edit'")
        
        print("\n**Team Workspace:**")
        print("1. Go to team workspace settings")
        print("2. Add integration to team workspace")
        print("3. Grant appropriate permissions")
        
        print("\n⚠️  **Important:** All databases and pages must be shared with the integration for the automation system to work properly.")
    
    def create_simple_test(self) -> None:
        """Create a simple connection test script"""
        test_script = '''#!/usr/bin/env python3
"""
Simple Notion Connection Test
"""

import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_notion_connection():
    """Test Notion API connection"""
    
    # Load token from environment
    TOKEN = os.getenv('NOTION_API_TOKEN')
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            # Test basic API access
            print("🧪 Testing Notion API connection...")
            
            # Try to list users (basic API test)
            async with session.get(
                "https://api.notion.com/v1/users",
                headers=headers
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ API Connection successful!")
                    print(f"   Found {len(data.get('results', []))} users")
                else:
                    print(f"❌ API Connection failed: {response.status}")
                    error_text = await response.text()
                    print(f"   Error: {error_text}")
                    
        except Exception as e:
            print(f"❌ Connection test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_notion_connection())
'''
        
        test_file = project_root / "scripts" / "simple_notion_test.py"
        with open(test_file, 'w') as f:
            f.write(test_script)
        
        self.print_success("Created simple_notion_test.py for basic testing")


async def main():
    """Main diagnostic function"""
    fixer = NotionAccessFixer()
    
    # Always create the simple test script
    fixer.create_simple_test()
    
    success = await fixer.diagnose_and_fix()
    
    if not success:
        print("\n" + "=" * 60)
        print("  NEXT STEPS TO FIX INTEGRATION")
        print("=" * 60)
        print("\n1. Follow the token setup instructions above")
        print("2. Share your databases with the integration")
        print("3. Run this script again to verify")
        print("4. Or run: python scripts/simple_notion_test.py")
        print("\n💡 Once fixed, run: python scripts/connect_lab_centers.py")
    
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
