# AI Core: Conversational AI System

Sebuah sistem AI percakapan modular yang menggunakan Google Gemini API. Proyek ini dirancang sebagai "AI Brain" yang dapat berpikir, mengingat, dan merespons secara alami dalam Bahasa Indonesia.

## Konsep Arsitektur

Sistem ini menggunakan pendekatan modular yang memisahkan logika berpikir, penyimpanan ingatan, dan antarmuka interaksi:

1.  **Interface (`app.py`)**: Titik masuk utama aplikasi (CLI) yang menangani input/output pengguna dan koordinasi antar modul.
2.  **Brain (`brain.py`)**: Inti dari AI yang membungkus model Gemini 1.5 Flash. Bertugas memproses input berdasarkan konteks yang diberikan (pendek & panjang) dan instruksi sistem.
3.  **Short-Term Memory (`memory.py`)**: Mengelola ingatan jangka pendek dengan sistem *rolling window* untuk menjaga percakapan tetap relevan.
4.  **Long-Term Memory (`long_memory.py`)**: Mengelola pengetahuan permanen menggunakan vector embeddings (FAISS) untuk pencarian kemiripan semantik.

**Inspirasi**: Arsitektur sistem ini terinspirasi oleh konsep "autonomous AI core" seperti pada sistem Neuro-sama, namun difokuskan sebagai asisten AI umum yang cerdas dan netral.

---

## Stage 2: Long-Term Memory (LTM)

Sistem kini mendukung Ingatan Jangka Panjang yang memungkinkan AI untuk mengingat informasi penting secara permanen di luar batas sesi chat saat ini.

### Cara Kerja
- **Short-Term Memory (STM)**: Mengingat pesan-pesan terakhir dalam sesi chat yang sedang berlangsung.
- **Long-Term Memory (LTM)**: Mengambil informasi relevan dari basis data lokal berdasarkan kemiripan makna menggunakan *Vector Embeddings*. Saat Anda bertanya, sistem akan mencari informasi terkait di LTM dan memberikannya kepada AI sebagai konteks tambahan.

### Cara Menambahkan Memori Jangka Panjang
Anda dapat menambahkan pengetahuan baru ke dalam sistem menggunakan skrip `ingest.py`:

```bash
# Menambahkan satu kalimat/teks
python ingest.py "Jules adalah asisten AI yang ahli dalam pengembangan perangkat lunak."

# Menambahkan dari file teks
python ingest.py --file data_pengetahuan.txt
```

---

## Prasyarat

- Python 3.9 atau lebih tinggi.
- API Key Google Gemini.

## Instalasi

1.  Pasang dependensi yang diperlukan:
    ```bash
    pip install -r requirements.txt
    ```

2.  Salin file `.env.example` menjadi `.env` dan masukkan API Key Anda.

## Cara Menjalankan

Jalankan sistem dengan perintah berikut:

```bash
python app.py
```

## Fitur

- **Semantic Search**: Pencarian informasi berdasarkan makna, bukan hanya kata kunci.
- **Persistence**: Ingatan jangka panjang disimpan secara lokal di direktori `ltm_data/`.
- **Indonesian Support**: Menggunakan model embedding multilingual untuk dukungan Bahasa Indonesia yang optimal.
