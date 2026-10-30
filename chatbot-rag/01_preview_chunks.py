from pathlib import Path

path = Path(__file__).resolve().parent / 'knowledge' / 'panduan_layanan.txt'
text = path.read_text(encoding='utf-8')
chunks = [item.strip() for item in text.split('\n\n') if item.strip()]

print('Jumlah chunk:', len(chunks))
for number, chunk in enumerate(chunks, start=1):
    print(f'\n[D{number}] ({len(chunk)} karakter)')
    print(chunk[:200])
