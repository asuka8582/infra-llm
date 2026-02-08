# AI Core: Conversational AI System

Sebuah sistem AI percakapan modular yang menggunakan Google Gemini API. Proyek ini dirancang sebagai "AI Brain" yang dapat berpikir, mengingat, dan merespons secara alami dalam Bahasa Indonesia.

## Konsep Arsitektur

Sistem ini menggunakan pendekatan modular yang memisahkan logika berpikir, penyimpanan ingatan, dan antarmuka interaksi:

1.  **Interface (`app.py`)**: Titik masuk utama aplikasi (CLI).
2.  **Brain (`brain.py`)**: Inti dari AI yang mengoordinasikan penalaran dan eksekusi tool.
3.  **Reasoning Layer (`reasoning.py`)**: Lapisan kontrol yang memaksa AI untuk berpikir langkah-demi-langkah.
4.  **Tools (`tools.py`)**: Kumpulan alat yang divalidasi dan aman untuk berinteraksi dengan dunia luar.
5.  **Memory**:
    - **Short-Term (`memory.py`)**: Ingatan sesi chat saat ini.
    - **Long-Term (`long_memory.py`)**: Pengetahuan permanen berbasis vector search.

---

## Stage 4: Tools & Actions

Sistem kini memiliki kemampuan untuk mengambil tindakan melalui Tool yang terkontrol. AI dapat mencari informasi di web, mengelola file di sandbox, dan menjalankan perintah terbatas.

### Daftar Tool
- `web_search`: Mencari informasi terbaru di internet.
- `read_file` / `write_file`: Membaca dan menulis file di dalam direktori `sandbox/`.
- `list_directory`: Melihat isi direktori sandbox.
- `run_command`: Menjalankan perintah sistem terbatas (`ls`, `pwd`, `python`, `pip list`).
- `write_memory`: Menyimpan fakta penting secara permanen ke memori jangka panjang.

### Batasan Keamanan (Safety Boundaries)
1.  **Sandbox Only**: Semua operasi file hanya diizinkan di dalam folder `sandbox/`. AI tidak bisa mengakses file sistem di luar folder ini.
2.  **Command Whitelist**: Hanya perintah tertentu yang diizinkan. Perintah berbahaya atau tidak dikenal akan ditolak.
3.  **Single Tool Call**: AI hanya dapat memanggil maksimal satu tool per input pengguna untuk menjaga kontrol.
4.  **Non-Autonomous**: AI tidak dapat menjalankan loop tindakan sendiri; setiap tindakan harus dipicu oleh interaksi pengguna.

---

## Stage 3: Reasoning & Control Layer
AI melakukan penalaran internal sebelum menjawab. Proses ini disembunyikan dari pengguna untuk menjaga jawaban tetap bersih dan fokus pada hasil akhir.

## Stage 2: Long-Term Memory (LTM)
Mendukung penyimpanan pengetahuan permanen. Gunakan `ingest.py` untuk menambahkan data secara manual.

---

## Prasyarat
- Python 3.9+
- API Key Google Gemini

## Instalasi
1. Pasang dependensi: `pip install -r requirements.txt`
2. Salin `.env.example` ke `.env` dan masukkan API Key Anda.

## Cara Menjalankan
```bash
python app.py
```
Semua file yang dihasilkan AI melalui tool `write_file` akan muncul di folder `sandbox/`.
