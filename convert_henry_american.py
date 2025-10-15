import asyncio
import edge_tts
import PyPDF2
import os

async def convert():
    pdf_path = "/Users/ugochi141/Desktop/Lab/Managment/Henry's Clinical Diagnosis and Management by Laboratory .pdf"
    
    print(f"📖 Reading: Henry's Clinical Diagnosis...")
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        total = len(pdf_reader.pages)
        print(f"📄 Processing {total} pages...")
        
        for i, page in enumerate(pdf_reader.pages, 1):
            text += page.extract_text() + "\n"
            if i % 50 == 0:
                print(f"   Processed {i}/{total} pages...")
    
    print(f"✅ Extracted {len(text):,} characters")
    
    # American male voice - Christopher (professional)
    voice = "en-US-ChristopherNeural"
    print("🎤 Using American male voice (Christopher)")
    
    output = "Henrys_Clinical_American_Male.mp3"
    print("⏳ Converting to audiobook...")
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output)
    
    size_mb = os.path.getsize(output) / (1024*1024)
    print(f"✅ Success! Saved as: {output}")
    print(f"📊 File size: {size_mb:.2f} MB")

asyncio.run(convert())
