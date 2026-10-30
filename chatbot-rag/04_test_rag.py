from rag_core import answer_with_rag

question = input('Tuliskan pertanyaan tentang dokumen: ').strip()
if not question:
    raise SystemExit('Pertanyaan tidak boleh kosong.')
result = answer_with_rag(question)
print('\nJawaban chatbot RAG:\n', result['answer'])
print('\nChunk yang digunakan:', [f"D{x['id']}" for x in result['sources']])
