from rag_core import retrieve

question = 'Bagaimana melaporkan komputer laboratorium yang rusak?'
print('Pertanyaan:', question)
for item in retrieve(question, top_k=3):
    print(f"\n[D{item['id']}] Skor kemiripan: {item['score']:.3f}")
    print(item['text'][:240])
