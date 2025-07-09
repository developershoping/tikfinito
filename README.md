# Tikfinito 🎙️
### Asisten AI Canggih untuk Live Streaming TikTok dengan Arsitektur P2P

Tikfinito adalah sebuah proyek inovatif yang menghadirkan asisten AI interaktif langsung ke dalam siaran langsung TikTok Anda. Asisten ini mampu membaca komentar chat secara real-time dan memberikan respon suara yang dihasilkan oleh AI Google Gemini.

Yang membedakan Tikfinito adalah penggunaan arsitektur **Peer-to-Peer (P2P)** canggih menggunakan WebRTC (via PeerJS). Ini memungkinkan Anda untuk menjalankan "otak" AI di komputer lokal Anda, sementara penonton dari seluruh dunia dapat terhubung dan mendengarkan siaran AI tanpa memerlukan hosting backend publik yang rumit atau layanan tunneling seperti `ngrok`.


*(Anda bisa mengganti URL gambar ini dengan screenshot aplikasi Anda saat berjalan)*

---

## 🏛️ Arsitektur Proyek

Proyek ini menggunakan arsitektur terpisah yang cerdas untuk membagi tugas:

1.  **Backend (`server.py`): "Studio Rekaman"**
    *   Berjalan secara lokal di komputer Anda.
    *   Menggunakan **Flask** untuk membuat API lokal.
    *   Terhubung ke **TikTok Live** untuk mendengarkan semua event (komentar, join, dll).
    *   Memanggil **Google Gemini API** untuk menghasilkan respon teks cerdas.
    *   Menyimpan seluruh riwayat log dan status koneksi di memori.

2.  **Halaman Host (`host.html`): "Menara Pemancar Radio"**
    *   **Anda buka secara lokal di browser Anda.**
    *   Terhubung ke `server.py` untuk mengambil data log terbaru.
    *   Menggunakan **PeerJS** untuk membuat "Room" P2P dengan ID unik.
    *   Menjadi pusat distribusi yang menyiarkan (broadcast) semua data dari server ke semua penonton yang terhubung.

3.  **Halaman Penonton (`index.html`): "Radio Penonton"**
    *   **Dihosting secara publik** (misalnya di GitHub Pages).
    *   Penonton hanya perlu memasukkan "Room ID" untuk "menyetel frekuensi".
    *   Terhubung langsung ke browser Anda (Host) melalui koneksi P2P.
    *   Menerima siaran data, menampilkannya sebagai log, dan menggunakan fitur suara browser untuk membacakan respon AI.

---

## ✨ Fitur Utama

-   **Respon Suara Real-time:** AI merespon komentar dengan suara yang alami.
-   **Arsitektur Peer-to-Peer (P2P):** Tidak perlu `ngrok` atau hosting backend. Sangat efisien dan aman.
-   **Antrian Suara Cerdas:** Respon suara tidak tumpang tindih, melainkan diucapkan satu per satu secara berurutan.
-   **Mudah Dibagikan:** Cukup bagikan URL GitHub Pages Anda dan sebuah Room ID agar orang lain bisa ikut mendengarkan.
-   **Konfigurasi Aman:** Kunci API disimpan dengan aman di file `.env` dan tidak pernah terekspos ke publik.
-   **Kontrol Penuh:** Anda sebagai host memiliki kontrol penuh untuk memulai dan memantau koneksi.

---

## 🛠️ Teknologi yang Digunakan

| Backend (Lokal) | Frontend (Browser) |
| :--- | :--- |
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) |
| ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) | ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) |
| `TikTokLive` | ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) |
| `google-generativeai` | `PeerJS` (WebRTC) |
| `python-dotenv` | `Web Speech API` |

---

## 🚀 Instalasi & Konfigurasi

Ikuti langkah-langkah ini untuk menyiapkan proyek di komputer Anda.

**1. Clone Repository**
```bash
git clone https://github.com/developershoping/tikfinito.git
cd tikfinito
```

**2. Buat File `requirements.txt`**
Buat sebuah file bernama `requirements.txt` dan isi dengan dependensi berikut:
```
google-generativeai
TikTokLive==8.0.0
python-dotenv
Flask
Flask-Cors
```

**3. Instal Dependensi Python**
Jalankan perintah ini di terminal Anda:
```bash
pip install -r requirements.txt
```

**4. Siapkan Kunci API (`.env`)**
Buat sebuah file bernama `.env` di dalam folder proyek. Buka file tersebut dan tambahkan kunci API Google Gemini Anda.
```
# .env
GEMINI_API_KEY="AIzaSy...KUNCI_RAHASIA_ANDA"
```
**PENTING:** Jangan pernah membagikan atau meng-upload file `.env` ini ke GitHub.

**5. Hosting Halaman Penonton (`index.html`)**
-   Buka repository `tikfinito` Anda di GitHub.
-   Pergi ke `Settings` > `Pages`.
-   Di bawah "Branch", pilih `main` (atau branch utama Anda) dan folder `/root`.
-   Klik `Save`. GitHub akan memberikan Anda URL publik untuk halaman Anda (misalnya: `https://developershoping.github.io/tikfinito/`). Anda perlu mengganti `index.html` dengan nama file penonton Anda jika berbeda.

---

## 💡 Cara Menjalankan

Untuk memulai sebuah sesi, Anda perlu menjalankan backend dan halaman host.

**1. Jalankan Server Backend**
Buka terminal di folder proyek Anda dan jalankan:
```bash
python server.py
```
Biarkan terminal ini tetap terbuka. Ia adalah "otak" dari AI Anda.

**2. Buka Halaman Host**
-   Di komputer yang sama, buka file `host.html` langsung di browser Anda (cukup double-click filenya).

**3. Mulai Sesi P2P**
-   Di halaman `host.html` yang terbuka, ketik sebuah **Room ID** yang unik (contoh: `live-gaming-malam-ini`).
-   Klik tombol **"Mulai Sebagai Host"**.

**4. Mulai Koneksi ke TikTok**
-   Setelah Host aktif, masukkan **@username** dari akun TikTok yang sedang live.
-   Klik **"Mulai Koneksi TikTok"**.
-   Anda akan melihat log komentar dan respon AI mulai muncul di halaman host.

**5. Bagikan ke Penonton**
-   Berikan **URL GitHub Pages** Anda (dari langkah konfigurasi) dan **Room ID** yang Anda buat kepada penonton.
-   Saat mereka membuka URL dan memasukkan Room ID, mereka akan langsung terhubung ke sesi Anda dan mulai mendengar siaran AI.

---

## 📝 Catatan Penting

-   **Firewall:** Jika Anda menjalankan ini pertama kali, Windows Firewall mungkin akan meminta izin untuk `python.exe`. Pastikan Anda **mengizinkan akses (Allow access)** agar arsitektur ini berfungsi.
-   **Kestabilan Koneksi:** Kualitas siaran ke penonton bergantung pada kestabilan koneksi internet Anda sebagai Host.

---

## 🤝 Kontribusi

Merasa ada yang bisa ditingkatkan? Pull requests sangat diterima. Untuk perubahan besar, silakan buka issue terlebih dahulu untuk mendiskusikan apa yang ingin Anda ubah.

## 📄 Lisensi

Didistribusikan di bawah Lisensi MIT.
