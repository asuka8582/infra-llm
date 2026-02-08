# AI Core: Conversational AI System

Sebuah sistem AI percakapan modular yang menggunakan Google Gemini API. Proyek ini dirancang sebagai "AI Brain" yang dapat berpikir, mengingat, dan merespons secara alami dalam Bahasa Indonesia.

## Konsep Arsitektur

Sistem ini menggunakan pendekatan modular yang memisahkan logika berpikir, penyimpanan ingatan, dan antarmuka interaksi:

1.  **Interface (`app.py`)**: Titik masuk utama aplikasi (CLI).
2.  **Brain (`brain.py`)**: Inti dari AI yang mengoordinasikan penalaran, validasi, dan eksekusi tool.
3.  **Reasoning Layer (`reasoning.py`)**: Lapisan kontrol yang memaksa AI untuk berpikir langkah-demi-langkah dan memvalidasi jawabannya sendiri.
4.  **Tools (`tools.py`)**: Kumpulan alat yang divalidasi dan aman untuk berinteraksi dengan dunia luar.
5.  **Memory**:
    - **Short-Term (`memory.py`)**: Ingatan sesi chat saat ini.
    - **Long-Term (`long_memory.py`)**: Pengetahuan permanen berbasis vector search dengan skor kepentingan.

---

## Stage 5: LLM Quality Improvement

Sistem kini lebih cerdas dan konsisten berkat peningkatan arsitektur prompt dan proses validasi internal.

### Peningkatan Utama:
- **Prompt Architecture**: Pemisahan yang jelas antara Aturan Sistem, Konteks Memori, dan Input Pengguna untuk hasil yang lebih fokus.
- **Self-Validation**: Sebelum menjawab, AI secara internal membuat draft jawaban, meninjaunya (validasi), dan memperbaikinya jika ditemukan ketidakkonsistenan. Hanya jawaban akhir yang telah divalidasi yang ditampilkan ke pengguna.
- **Importance Scoring**: Informasi yang disimpan di memori jangka panjang kini memiliki skor kepentingan (1-10). Informasi yang dianggap tidak penting (skor < 3) akan diabaikan untuk menjaga kualitas memori.
- **Consistency Guard**: Instruksi kualitas yang ketat untuk menjaga nada bicara Bahasa Indonesia yang profesional dan mencegah halusinasi.

---

## Stage 4: Tools & Actions
Sistem dapat mencari informasi di web, mengelola file di sandbox, dan menjalankan perintah terbatas. Semua operasi file dibatasi di folder `sandbox/`.

## Stage 2: Long-Term Memory (LTM)
Mendukung penyimpanan pengetahuan permanen berbasis kemiripan semantik.

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
