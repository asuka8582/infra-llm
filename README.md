# AI Core: Conversational AI System

Sebuah sistem AI percakapan modular yang menggunakan Google Gemini API. Proyek ini dirancang sebagai "AI Brain" yang dapat berpikir, mengingat, dan merespons secara alami dalam Bahasa Indonesia.

## Konsep Arsitektur

Sistem ini menggunakan pendekatan modular yang memisahkan logika berpikir, penyimpanan ingatan, dan antarmuka interaksi:

1.  **Interface (`app.py`)**: Titik masuk utama aplikasi (CLI) yang menangani input/output pengguna dan koordinasi antar modul.
2.  **Brain (`brain.py`)**: Inti dari AI yang membungkus model Gemini 1.5 Flash dan mengoordinasikan lapisan penalaran.
3.  **Reasoning Layer (`reasoning.py`)**: Lapisan kontrol yang memaksa AI untuk berpikir langkah-demi-langkah sebelum memberikan jawaban akhir.
4.  **Short-Term Memory (`memory.py`)**: Mengelola ingatan jangka pendek dengan sistem *rolling window*.
5.  **Long-Term Memory (`long_memory.py`)**: Mengelola pengetahuan permanen menggunakan vector embeddings (FAISS).

**Inspirasi**: Arsitektur sistem ini terinspirasi oleh konsep "autonomous AI core" seperti pada sistem Neuro-sama, namun difokuskan sebagai asisten AI umum yang cerdas dan netral.

---

## Stage 3: Reasoning & Control Layer

Sistem kini dilengkapi dengan lapisan penalaran internal untuk meningkatkan konsistensi dan kualitas jawaban.

### Cara Kerja
Setiap kali pengguna memberikan input, AI tidak langsung menjawab. Sebaliknya, AI akan:
1.  **Menganalisis Niat**: Memahami apa yang sebenarnya diinginkan pengguna.
2.  **Evaluasi Konteks**: Memeriksa memori jangka pendek dan panjang untuk informasi relevan.
3.  **Perencanaan**: Menyusun langkah-langkah untuk memberikan jawaban terbaik.
4.  **Output Terkontrol**: Menghasilkan jawaban akhir berdasarkan proses penalaran tersebut.

### Perbedaan Output
- **Raw LLM Output**: AI memberikan jawaban langsung (mungkin kurang konsisten).
- **Controlled Reasoning-based Output**: AI berpikir secara internal terlebih dahulu. Hasil penalaran ini **disembunyikan** dari pengguna, sehingga pengguna hanya menerima jawaban akhir yang lebih matang dan terstruktur.

---

## Stage 2: Long-Term Memory (LTM)

Sistem mendukung Ingatan Jangka Panjang yang memungkinkan AI untuk mengingat informasi penting secara permanen.

### Cara Menambahkan Memori Jangka Panjang
Gunakan skrip `ingest.py`:
```bash
python ingest.py "Teks pengetahuan di sini"
```

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
