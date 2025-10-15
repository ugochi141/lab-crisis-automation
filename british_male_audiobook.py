import asyncio
import edge_tts
import PyPDF2
import sys
import os

async def convert_to_british_male(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Error: File not found!")
        return
    
    print(f"📖 Reading: {os.path.basename(pdf_path)}")
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        total = len(pdf_reader.pages)
        print(f"📄 Processing {total} pages...")
        
        for i, page in enumerate(pdf_reader.pages, 1):
            text += page.extract_text() + "\n"
            if i % 50 == 0:
                print(f"   Processed {i}/{total} pages...")
    
    print(f"✅ Extracted {len(text)} characters")
    
    # British Male voice
    voice = "en-GB-RyanNeural"
    print(f"🎤 Using British Male voice: Ryan")
    
    output = pdf_path.replace('.pdf', '_british_male.mp3')
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output)
    print(f"✅ Saved to: {output}")

asyncio.run(convert_to_british_male(sys.argv[1]))
