<!doctype html>
<html lang="id"><meta charset="utf-8"><title>Uji koneksi Laragon dan Flask</title>
<h1>Uji komunikasi Laragon - Flask</h1><form id="test-form"><label for="question">Pertanyaan</label><input id="question" value="Halo dari Laragon" required><button>Kirim ke Flask</button></form><pre id="result">Belum ada respons.</pre>
<script>document.getElementById('test-form').addEventListener('submit',async e=>{e.preventDefault();const out=document.getElementById('result');try{const r=await fetch('chat.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:document.getElementById('question').value})});out.textContent=JSON.stringify(await r.json(),null,2)}catch(e){out.textContent=e.message}});</script></html>
