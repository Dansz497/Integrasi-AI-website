from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16384


@app.get('/api/health')
def health():
    return jsonify(status='ok', service='Flask Chatbot API')


@app.post('/api/chat')
def chat():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get('question'), str):
        return jsonify(error='Pertanyaan wajib berupa teks.'), 400
    question = data['question'].strip()
    if not question or len(question) > 500:
        return jsonify(error='Pertanyaan wajib diisi (maks. 500 karakter).'), 400
    return jsonify(answer='Balasan uji Flask: ' + question, sources=[])
