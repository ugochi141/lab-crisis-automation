import asyncio
import edge_tts
import PyPDF2

async def main():
    with open("/Users/ugochi141/henry.pdf", 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    
    voice = "en-GB-RyanNeural"  # British male
    tts = edge_tts.Communicate(text, voice)
    await tts.save("henry_british.mp3")
    print("Done! Saved as henry_british.mp3")

asyncio.run(main())
