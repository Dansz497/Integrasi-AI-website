"""Pemeriksaan lokal; tidak memakai kuota API."""
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parent
result = subprocess.run([sys.executable, str(BASE / '01_preview_chunks.py')], capture_output=True, text=True)
assert result.returncode == 0, result.stderr
assert 'Jumlah chunk: 9' in result.stdout, result.stdout
print('PASS: dokumen menghasilkan 9 chunk')
assert (BASE / '02_build_index.py').exists(), 'B3: program pembuat indeks belum ada'
if '--index' in sys.argv:
    import json
    import numpy as np
    metadata = json.loads((BASE / 'index/chunks.json').read_text(encoding='utf-8'))
    vectors = np.load(BASE / 'index/embeddings.npy', allow_pickle=False)
    assert len(metadata['chunks']) == len(vectors) == 9
    assert vectors.ndim == 2 and np.isfinite(vectors).all()
    assert (np.linalg.norm(vectors, axis=1) > 0).all()
    print('PASS: 9 vektor valid, dimensi', vectors.shape[1])
assert (BASE / 'rag_core.py').exists(), 'B4: retrieval belum ada'
from api_app import app
client = app.test_client()
assert client.get('/api/health').json['status'] == 'ok'
for payload in ({}, {'question': ''}, {'question': 'x' * 501}, [], {'question': 123}):
    assert client.post('/api/chat', json=payload).status_code == 400, payload
assert client.get('/api/chat').status_code == 405
print('PASS: health, validasi input, metode HTTP')
