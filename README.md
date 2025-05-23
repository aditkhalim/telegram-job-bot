# Telegram Job & CV Roasting Bot

Bot Telegram multifungsi untuk membantu pencari kerja — mulai dari pencarian lowongan, info magang, hingga fitur roasting CV yang sarkas dan menyentil 😄.

---

## 🚀 Fitur Utama

### 🔍 /cari
Cari lowongan kerja berdasarkan keyword, hasil dari [Jooble API](https://jooble.org/). Lokasi default: **Indonesia**.

### 📄 /roasting
Upload file CV dalam format PDF atau DOCX, dan bot akan "merosting" CV tersebut dengan AI dari [OpenRouter](https://openrouter.ai). Gaya bahasanya sarkas dan blak-blakan, cocok untuk refleksi dan hiburan 🤖

### 📅 /event
Tampilkan agenda job fair yang akan datang di Indonesia dari sumber-sumber kredibel (ECC UGM, Kemnaker, dsb).

### 🧑‍🎓 /magang
Menampilkan program magang terbaru dari BUMN, LPS, Bank Indonesia, dan lainnya.

### 💡 /motivasi
Memberikan motivasi sarkas dan realistis untuk para pejuang kerja.

---

## 🧰 Teknologi yang Digunakan

- Python `3.x`
- [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot)
- Jooble API (lowongan kerja)
- OpenRouter (untuk AI Chat Completion)
- `PyPDF2`, `python-docx`, `dotenv`, `FPDF`

---

## 📁 Struktur Proyek (minimal)

```
project-folder/
│
├── main.py              # Bot utama
├── .env                 # Simpan token dan API key
├── requirements.txt     # Dependensi
└── README.md            # Dokumentasi
```

---

## 🔧 Cara Menjalankan

1. Clone repo ini:
```bash
git clone https://github.com/username/telegram-job-bot.git
cd telegram-job-bot
```

2. Install dependency:
```bash
pip install -r requirements.txt
```

3. Siapkan file `.env`:
```
TELEGRAM_BOT_TOKEN=xxxxx
JOOBLE_API_KEY=xxxxx
OPENROUTER_API_KEY=xxxxx
```

4. Jalankan:
```bash
python main.py
```

---

## ⚠️ Keterbatasan

- Belum menggunakan database permanen
- Berjalan via polling, belum deploy ke server/hosting
- Fitur masih terus dikembangkan dan eksperimen

---

## 💬 Tujuan Proyek

Proyek ini saya buat untuk menggabungkan teknologi AI dengan kebutuhan sehari-hari, sekaligus dijadikan bahan portofolio yang praktis dan menyenangkan.

Silakan dicoba, fork, atau beri saran jika kamu punya ide! 🙌

---

**Dibuat oleh:** [Adit Nur K] — powered by kopi dan semangat cari kerja ☕
