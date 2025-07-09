# server.py

import os
import google.generativeai as genai
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, GiftEvent, JoinEvent
import time
import asyncio
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import socket

# --- FUNGSI UNTUK MENDAPATKAN IP LOKAL ---
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1)); IP = s.getsockname()[0]
    except Exception: IP = '127.0.0.1'
    finally: s.close()
    return IP

# --- KONFIGURASI ---
load_dotenv()
app = Flask(__name__)
CORS(app) # Mengizinkan koneksi dari sumber manapun (penting untuk P2P)

# --- STATE (Kondisi Aplikasi yang Disimpan di Memori) ---
app_state = {
    "log_items": [],
    "tiktok_status": "Idle", # Status: Idle, Connecting, Connected, Error
    "last_update": time.time()
}

# --- Logika AI & TikTok ---
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: raise ValueError("GEMINI_API_KEY tidak ditemukan di file .env")
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"Error Konfigurasi Gemini: {e}")

def get_gemini_response(prompt: str) -> str:
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        system_prompt = "Anda adalah Gem, asisten AI yang ceria dan jenaka di TikTok. Jawablah dengan singkat (1-2 kalimat) dan sapa pengguna dengan nama mereka."
        full_prompt = f"{system_prompt}\n\nINPUT: {prompt}\n\nJAWABAN:"
        response = model.generate_content(full_prompt)
        return response.text.replace('*', '').strip()
    except Exception as e:
        print(f"Error Gemini API: {e}")
        return ""

# --- FUNGSI UNTUK DIJALANKAN DI THREAD TERPISAH ---
def run_tiktok_client(username: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TikTokLiveClient(unique_id=f"@{username}")

    def add_log(log_type, data):
        global app_state
        app_state["log_items"].append({"type": log_type, "data": data, "timestamp": time.time()})
        if len(app_state["log_items"]) > 200: app_state["log_items"].pop(0) # Batasi log
        app_state["last_update"] = time.time()

    @client.on(CommentEvent)
    async def on_comment(event: CommentEvent):
        print(f"[Komentar] {event.user.nickname}: {event.comment}")
        add_log("comment", {"user": event.user.nickname, "text": event.comment})
        prompt = f"Pengguna '{event.user.nickname}' berkomentar: '{event.comment}'"
        ai_response = get_gemini_response(prompt)
        if ai_response:
            print(f"🤖 Respon Gemini: {ai_response}")
            add_log("ai_response", {"text": ai_response})
    
    @client.on("connect")
    async def on_connect(_): app_state["tiktok_status"] = "Connected"; add_log("status", {"message": f"Berhasil terhubung ke @{client.unique_id}!"}); print(f"Berhasil terhubung ke @{client.unique_id}!")
    @client.on("disconnect")
    async def on_disconnect(_): app_state["tiktok_status"] = "Idle"; add_log("status", {"message": "Koneksi terputus."}); print("Koneksi TikTok terputus.")

    try:
        app_state["tiktok_status"] = "Connecting"
        client.run()
    except Exception as e:
        app_state["tiktok_status"] = "Error"; add_log("status", {"message": f"Error koneksi: {e}"}); print(f"Error saat menjalankan TikTok client: {e}")

# --- API ENDPOINTS ---
@app.route('/api/status')
def get_status(): return jsonify(app_state)

@app.route('/api/start', methods=['POST'])
def start_tiktok():
    if app_state["tiktok_status"] in ["Connecting", "Connected"]: return jsonify({"message": "Koneksi sudah berjalan."}), 400
    data = request.get_json(); username = data.get('username')
    if not username: return jsonify({"error": "Username tidak boleh kosong"}), 400
    # Jalankan client di thread terpisah agar tidak memblokir Flask
    threading.Thread(target=run_tiktok_client, args=(username,), daemon=True).start()
    return jsonify({"message": f"Mencoba terhubung ke @{username}..."})

if __name__ == '__main__':
    port = 5000
    host = "127.0.0.1" # Cukup listen di localhost, P2P akan menanganinya
    print("="*40)
    print("Server API Flask Lokal Berjalan!")
    print(f"Backend siap di: http://{host}:{port}")
    print("Selanjutnya, buka file 'host.html' di browser Anda.")
    print("="*40)
    app.run(host=host, port=port, debug=False)
