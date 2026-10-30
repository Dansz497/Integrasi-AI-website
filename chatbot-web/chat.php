<?php
header('Content-Type: application/json; charset=utf-8');
function fail($status, $message) { http_response_code($status); echo json_encode(['error' => $message]); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail(405, 'Gunakan metode POST.');
$raw = file_get_contents('php://input', false, null, 0, 16385);
if (strlen($raw) > 16384) fail(413, 'Permintaan terlalu besar.');
$data = json_decode($raw, true);
if (!is_array($data) || !isset($data['question']) || !is_string($data['question'])) fail(400, 'Pertanyaan wajib berupa teks.');
$question = trim($data['question']);
if ($question === '' || mb_strlen($question, 'UTF-8') > 500) fail(400, 'Pertanyaan wajib diisi (maks. 500 karakter).');
if (!function_exists('curl_init')) fail(500, 'Ekstensi PHP cURL belum aktif.');
$ch = curl_init('http://127.0.0.1:5001/api/chat');
curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_RETURNTRANSFER => true,
CURLOPT_HTTPHEADER => ['Content-Type: application/json'], CURLOPT_POSTFIELDS => json_encode(['question' => $question]),
CURLOPT_CONNECTTIMEOUT => 5, CURLOPT_TIMEOUT => 90]);
$response = curl_exec($ch);
$status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
if ($response === false) fail(502, 'Flask tidak dapat dihubungi.');
if (!is_array(json_decode($response, true))) fail(502, 'Respons Flask bukan JSON yang valid.');
http_response_code($status >= 100 && $status <= 599 ? $status : 502);
echo $response;
