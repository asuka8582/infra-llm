# AI Core: Conversational AI System

Sebuah sistem AI percakapan modular yang menggunakan Google Gemini API. Proyek ini dirancang sebagai "AI Brain" yang dapat berpikir, merencanakan, mengingat, dan merespons secara alami dalam Bahasa Indonesia.

## Konsep Arsitektur

Sistem ini menggunakan pendekatan modular yang memisahkan logika berpikir, perencanaan, penyimpanan ingatan, dan antarmuka interaksi:

1.  **Interface (`app.py`)**: Titik masuk utama aplikasi (CLI).
2.  **Brain (`brain.py`)**: Inti dari AI yang mengoordinasikan perencanaan, penalaran, dan eksekusi tool.
3.  **Planner Layer (`planner.py`)**: Mengelola pembuatan rencana internal langkah-demi-langkah sebelum menjawab.
4.  **Reasoning Layer (`reasoning.py`)**: Lapisan kontrol yang memaksa AI untuk menganalisis niat dan memvalidasi jawabannya sendiri.
5.  **Tools (`tools.py`)**: Kumpulan alat yang divalidasi dan aman untuk berinteraksi dengan dunia luar.
6.  **Memory**:
    - **Short-Term (`memory.py`)**: Ingatan sesi chat saat ini.
    - **Long-Term (`long_memory.py`)**: Pengetahuan permanen berbasis vector search dengan skor kepentingan.

---

## Stage 6: Planning & Multi-Step Thinking

Sistem kini dilengkapi dengan lapisan perencanaan internal untuk meningkatkan koherensi dan kedalaman jawaban.

### Cara Kerja
Sebelum memberikan jawaban akhir, AI akan secara internal melakukan:
1.  **Intent Analysis**: Memahami secara mendalam apa yang diinginkan oleh pengguna.
2.  **Plan Generation**: Menyusun daftar langkah terurut untuk menyelesaikan permintaan.
3.  **Step Execution**: Menjalankan rencana tersebut langkah demi langkah, termasuk penalaran logis dan penggunaan tool jika diperlukan.
4.  **Validation**: Memastikan jawaban akhir sesuai dengan rencana dan fakta yang tersedia.

Proses perencanaan dan eksekusi internal ini **disembunyikan** dari pengguna untuk menjaga interaksi tetap bersih, namun memberikan hasil yang lebih terstruktur dan andal.

---

## Stage 5: LLM Quality Improvement
Mendukung arsitektur prompt terstruktur, validasi mandiri, dan sistem skor kepentingan untuk memori jangka panjang.

## Stage 4: Tools & Actions
Sistem dapat mencari informasi di web, mengelola file di sandbox, dan menjalankan perintah terbatas.

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
