# AI Core: Conversational AI System

Sebuah sistem AI percakapan modular yang menggunakan Google Gemini API. Proyek ini dirancang sebagai "AI Brain" yang dapat berpikir, mengingat, dan merespons secara alami dalam Bahasa Indonesia.

## Konsep Arsitektur

Sistem ini menggunakan pendekatan modular yang memisahkan logika berpikir, penyimpanan ingatan, dan antarmuka interaksi:

1.  **Interface (`app.py`)**: Titik masuk utama aplikasi (CLI) yang menangani input/output pengguna dan koordinasi antar modul.
2.  **Brain (`brain.py`)**: Inti dari AI yang membungkus model Gemini 1.5 Flash. Bertugas memproses input berdasarkan konteks yang diberikan dan instruksi sistem (System Instruction).
3.  **Memory (`memory.py`)**: Mengelola ingatan jangka pendek (Short-Term Memory) dengan sistem *rolling window* untuk menjaga percakapan tetap relevan tanpa melebihi batas konteks.

**Inspirasi**: Arsitektur sistem ini terinspirasi oleh konsep "autonomous AI core" seperti pada sistem Neuro-sama, namun difokuskan sebagai asisten AI umum yang cerdas dan netral, bukan sebagai persona VTuber atau karakter tertentu.

## Prasyarat

- Python 3.9 atau lebih tinggi.
- API Key Google Gemini (dapat diperoleh di [Google AI Studio](https://aistudio.google.com/)).

## Instalasi

1.  Pasang dependensi yang diperlukan:
    ```bash
    pip install -r requirements.txt
    ```

2.  Salin file `.env.example` menjadi `.env`:
    ```bash
    cp .env.example .env
    ```

3.  Buka file `.env` dan masukkan API Key Anda:
    ```env
    GEMINI_API_KEY=AIzaSy... (API Key Anda)
    ```

## Cara Menjalankan

Jalankan sistem dengan perintah berikut:

```bash
python app.py
```

Setelah berjalan, Anda dapat mulai mengobrol dengan AI. Ketik `exit` atau `quit` untuk mematikan sistem.

## Fitur

- **Multi-turn Conversation**: AI mengingat konteks percakapan sebelumnya.
- **Indonesian Default**: Dioptimalkan untuk Bahasa Indonesia yang cerdas dan profesional.
- **Error Handling**: Menangani masalah koneksi API dan filter keamanan secara anggun.
- **Modular Design**: Komponen terpisah memudahkan pengembangan lebih lanjut (seperti penambahan modul suara atau penglihatan).
