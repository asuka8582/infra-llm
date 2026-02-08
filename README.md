# Gemini Chat CLI

Aplikasi chat sederhana menggunakan Google Gemini API (Gemini 1.5 Flash) berbasis CLI.

## Fitur
- Menggunakan model `gemini-1.5-flash`.
- Mendukung percakapan multi-turn (chat memory).
- Bahasa default: Bahasa Indonesia.
- Konfigurasi melalui file `.env`.

## Prasyarat
- Python 3.9+
- API Key dari [Google AI Studio](https://aistudio.google.com/)

## Instalasi

1. Klon repositori ini.
2. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Salin file `.env.example` menjadi `.env`:
   ```bash
   cp .env.example .env
   ```
4. Masukkan API Key Anda ke dalam file `.env`:
   ```env
   GEMINI_API_KEY=YOUR_API_KEY_HERE
   ```

## Cara Menjalankan

Jalankan aplikasi dengan perintah:
```bash
python app.py
```

Ketik `exit` atau `quit` untuk mengakhiri percakapan.
