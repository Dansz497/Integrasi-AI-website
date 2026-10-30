import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

load_dotenv(Path(__file__).resolve().parent / ".env")

if not os.getenv("GEMINI_API_KEY"):
    raise SystemExit("Isi GEMINI_API_KEY di file .env terlebih dahulu.")

client = genai.Client()
question = "Berapa lama proses surat aktif kuliah di Akademik Demo?"

response = client.models.generate_content(
    model=os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite"),
    contents=question,
)

print("Pertanyaan:", question)
print("Jawaban tanpa RAG:", response.text or "(Tidak ada teks jawaban)")
