import asyncio
import edge_tts
import PyPDF2
import sys
import os

async def convert_to_nigerian(pdf_path, voice_gender="female"):
    """
    Convert PDF to audiobook with Nigerian English accent
    voice_gender: "female" for Ezinne, "male" for Abeo
    """
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found!")
        return
    
    # Read PDF
    print(f"📖 Reading PDF: {pdf_path}")
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            total_pages = len(pdf_reader.pages)
            print(f"📄 Found {total_pages} pages")
            
            for i, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                if i % 10 == 0:
                    print(f"   Processed {i}/{total_pages} pages...")
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return
    
    if not text.strip():
        print("❌ No text found in PDF!")
        return
    
    print(f"✅ Extracted {len(text)} characters of text")
    
    # Choose Nigerian voice
    if voice_gender.lower() == "male":
        voice = "en-NG-AbeoNeural"  # Male Nigerian voice
        voice_name = "Abeo"
    else:
        voice = "en-NG-EzinneNeural"  # Female Nigerian voice
        voice_name = "Ezinne"
    
    print(f"🎤 Using Nigerian voice: {voice_name}")
    
    # Create output filename
    pdf_name = os.path.splitext(pdf_path)[0]
    output_path = f"{pdf_name}_nigerian_{voice_name}.mp3"
    
    # Convert to speech
    print("🔊 Converting to speech with Nigerian accent...")
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        print(f"✅ Success! Audiobook saved to: {output_path}")
        print(f"📁 File size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
    except Exception as e:
        print(f"❌ Error during conversion: {e}")

async def main():
    print("🇳🇬 Nigerian English PDF to Audiobook Converter")
    print("=" * 50)
    
    # Get arguments or use default
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
        voice = sys.argv[2] if len(sys.argv) > 2 else "female"
    else:
        # Interactive mode
        pdf_file = input("Enter PDF filename (or press Enter for 'book.pdf'): ").strip()
        if not pdf_file:
            pdf_file = "book.pdf"
        
        voice_choice = input("Choose voice - (f)emale or (m)ale? [default: female]: ").strip().lower()
        voice = "male" if voice_choice.startswith('m') else "female"
    
    await convert_to_nigerian(pdf_file, voice)

if __name__ == "__main__":
    asyncio.run(main())
