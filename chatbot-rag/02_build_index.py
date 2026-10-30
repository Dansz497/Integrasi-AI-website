import json
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / '.env')
text = (BASE / 'knowledge/panduan_layanan.txt').read_text(encoding='utf-8')
chunks = [item.strip() for item in text.split('\n\n') if item.strip()]
if not chunks:
    raise SystemExit('Dokumen kosong.')
client = genai.Client()
result = client.models.embed_content(
    model='gemini-embedding-001', contents=chunks,
    config=types.EmbedContentConfig(task_type='RETRIEVAL_DOCUMENT'),
)
vectors = np.asarray([item.values for item in result.embeddings], dtype=np.float32)
if vectors.ndim != 2 or len(vectors) != len(chunks) or not np.isfinite(vectors).all():
    raise RuntimeError('Embedding tidak valid; indeks lama tidak diubah.')
folder = BASE / 'index'
folder.mkdir(exist_ok=True)
metadata = {'embedding_model': 'gemini-embedding-001', 'source': 'panduan_layanan.txt',
            'chunks': [{'id': i + 1, 'text': chunk} for i, chunk in enumerate(chunks)]}
np.save(folder / 'embeddings.npy', vectors)
(folder / 'chunks.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Index berhasil dibuat: {len(chunks)} chunk, dimensi vektor {vectors.shape[1]}.')
print('File: index/chunks.json dan index/embeddings.npy')
