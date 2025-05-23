from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from docx import Document
import PyPDF2
import requests
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv
import os
import random

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MOTIVASI_LIST = [
    "CV kamu keren banget, sayang belum dikirim ke mana-mana.",
    "Jangan menyerah... kalau belum nyoba, nyerah dari apa?",
    "LinkedIn-mu aktif, tapi kok email belum dibales-bales ya?",
    "Lulus kuliah itu baru bab 1. Bab 2: cari kerja sambil waras.",
    "Kegagalan adalah bagian dari proses. Tapi kalau gagal terus, coba introspeksi juga.",
    "CV boleh 2 halaman, asal bukan isinya keluhan hidup.",
    "Interview gagal? Mungkin karena kamu jawabnya kayak skripsi, bukan ngobrol.",
    "Hidup ini keras, makanya CV-mu jangan lembek.",
    "Job fair itu bukan tempat jalan-jalan. Bawa CV, bukan harapan kosong.",
    "HRD juga manusia, jangan kasih mereka alasan buat skip kamu.",
    "Update CV-mu dulu, baru update story galaumu.",
    "Jangan cuma nunggu dipanggil. Apply terus, meski ditolak.",
    "Ngeluh boleh, asal sambil apply.",
    "CV yang bagus itu kayak mantan ideal — susah dicari, tapi berkesan.",
    "Kalau kamu males ngirim lamaran, jangan salahin semesta.",
    "Jangan menyerah, kecuali kamu disuruh resign.",
    "CV boleh 2 halaman, asal isinya bukan drama.",
    "LinkedIn itu etalase. Realitanya ya... tetap usaha.",
    "Gagal interview itu biasa. Nggak nyoba itu baru dosa.",
    "Loker impian itu nyata. Tapi yang ngisi ya orang yang rajin nyari."
]

# ==============================
# ======== DATA AGENDA ========
# ==============================
AGENDA_EVENT = [
    {
        "judul": "Career Days 30th – ECC UGM",
        "tanggal": "5–6 Juli 2025",
        "lokasi": "Yogyakarta",
        "link": "https://ecc.co.id/careerdays/home/index?type=employer"
    },
    {
        "judul": "UNNES Career Expo (UCE) 2025",
        "tanggal": "2–3 Juli 2025",
        "lokasi": "Gedung Prof. Wuryanto UNNES, Semarang",
        "link": "https://sites.unnes.ac.id/uce/"
    },
    {
        "judul": "Job Fair Bontang 2025",
        "tanggal": "21–25 Juli 2025",
        "lokasi": "Bontang",
        "link": "https://www.beritasiber.com/job-fair-bontang-2025"
    },
    {
        "judul": "Kemnaker Job Fair 2025",
        "tanggal": "22–23 Mei 2025",
        "lokasi": "Kementerian Ketenagakerjaan RI, Jakarta",
        "link": "https://jobfair.kemnaker.go.id/"
    }
]

AGENDA_MAGANG = [
    {
        "judul": "Program Magang Reguler Batch 2 – Pelindo Group",
        "periode": "Juli – Desember 2025",
        "pendaftaran": "19 Mei – 10 Juni 2025",
        "lokasi": "Berbagai lokasi operasional Pelindo",
        "link": "https://pelindo.co.id/media/706/program-magang-reguler-batch-2-tahun-2025-di-pelindo-group"
    },
    {
        "judul": "Magang Umum Batch 2 – PERURI",
        "periode": "6 bulan (Onsite)",
        "pendaftaran": "Hingga 25 Mei 2025",
        "lokasi": "Jakarta Selatan",
        "link": "https://magenta.bumn.go.id/lowongan?lokasi=3174&posting=12156"
    },
    {
        "judul": "Program Magang – Bank Indonesia",
        "periode": "Sesuai kesepakatan",
        "pendaftaran": "Sesuai MoU",
        "lokasi": "Kantor Bank Indonesia",
        "link": "https://www.bi.go.id/id/karier/internship-program.aspx"
    },
    {
        "judul": "Program Magang – PT Freeport Indonesia",
        "periode": "Sesuai program",
        "pendaftaran": "Sesuai jadwal",
        "lokasi": "Papua",
        "link": "https://ptfi.co.id/id/program-magang"
    },
    {
        "judul": "Program Magang – LPS",
        "periode": "Sesuai program",
        "pendaftaran": "Sesuai jadwal",
        "lokasi": "Kantor LPS",
        "link": "https://lps.go.id/karier/magang/"
    }
]

# ==============================
# ========== FITUR ============
# ==============================

def start(update, context):
    keyboard = [['/cari-loker', '/roasting CV'], ['/event job fair', '/magang'], ['/motivasi']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        "👋 Selamat datang di Bot Info Loker & Roasting CV dengan AI! \n\nGunakan tombol di bawah ini untuk menjelajahi fitur. Bot ini masih terus saya lakukan pengembangan dan mungkin akan ada penambahan menu kedepannya nanti.\n\nHope you enjoy this Bot, guys 😉 \n\nCreated By: Adit Nur K",
        reply_markup=reply_markup,
        reply_to_message_id=update.message.message_id
    )

def roasting_prompt(update, context):
    update.message.reply_text(
        "📄 Silakan kirim file CV kamu dalam format PDF atau DOCX untuk di-roasting oleh HRD sarkas. Maksimal 2MB ya!",
        reply_to_message_id=update.message.message_id
    )

def cari(update, context):
    args = context.args

    if not args:
        update.message.reply_text("Format: /cari <posisi yang dicari>\nContoh: /cari programmer",
        reply_to_message_id=update.message.message_id)
        return

    keyword = ' '.join(args)
    location = "Indonesia"

    payload = {"keywords": keyword, "location": location}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(f'https://jooble.org/api/{JOOBLE_API_KEY}', json=payload, headers=headers)
        data = response.json()
        jobs_raw = data.get('jobs', [])

        jobs = sorted(jobs_raw, key=lambda x: x.get('date', ''), reverse=True)
        if not jobs:
            update.message.reply_text("Tidak ada hasil ditemukan untuk posisi tersebut di Indonesia.",
            reply_to_message_id=update.message.message_id)
            return

        for job in jobs[:5]:
            update.message.reply_text(
                f"💼 {job.get('title')}\n"
                f"🏢 {job.get('company')}\n"
                f"📍 {job.get('location')}\n"
                f"🕒 {job.get('date')}\n"
                f"🔗 {job.get('link')}",
                reply_to_message_id=update.message.message_id
            )
    except Exception as e:
        update.message.reply_text(f"Terjadi error: {e}", reply_to_message_id=update.message.message_id)

def event(update, context):
    for e in AGENDA_EVENT:
        update.message.reply_text(
            f"📌 *{e['judul']}*\n🗓️ {e['tanggal']}\n📍 {e['lokasi']}\n🔗 {e['link']}",
            parse_mode='Markdown',
            reply_to_message_id=update.message.message_id
        )

def magang(update, context):
    for m in AGENDA_MAGANG:
        update.message.reply_text(
            f"📌 *{m['judul']}*\n📅 Periode: {m['periode']}\n📝 Pendaftaran: {m['pendaftaran']}\n📍 Lokasi: {m['lokasi']}\n🔗 {m['link']}",
            parse_mode='Markdown',
            reply_to_message_id=update.message.message_id
        )

def motivasi(update, context):
    pesan = random.choice(MOTIVASI_LIST)
    update.message.reply_text(
        f"💡 {pesan}",
        reply_to_message_id=update.message.message_id
    )

def roasting_cv(update, context):
    file = update.message.document
    filename = file.file_name.lower()

    # ✅ Cek apakah nama file mengandung 'cv'
    if "cv" not in filename:
        update.message.reply_text(
            "❗ Nama file harus mengandung kata 'CV'. Silakan kirim ulang file yang sesuai.",
            reply_to_message_id=update.message.message_id
        )
        return

    file_data = file.get_file().download_as_bytearray()
    text = extract_text_from_pdf(file_data) if filename.endswith('.pdf') else extract_text_from_docx(file_data)
    roasting = generate_roast_ai(text)

    update.message.reply_text(
        roasting,
        reply_to_message_id=update.message.message_id
    )


def extract_text_from_pdf(data):
    reader = PyPDF2.PdfReader(BytesIO(data))
    return "\n".join([page.extract_text() or "" for page in reader.pages])

def extract_text_from_docx(data):
    doc = Document(BytesIO(data))
    return "\n".join([p.text for p in doc.paragraphs])

def generate_roast_ai(cv_text):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://yourdomain.com",
        "X-Title": "Telegram Roasting CV Bot"
    }

    prompt = (
        "Kamu adalah HRD dari Indonesia yang sangat blak-blakan dan sarkastik. Nggak boleh dengan bahasa yang halus ya, kalau perlu pakai kalimat-kalimat perumpamaan\n"
        "Roasting CV ini dengan Bahasa Indonesia maksimal 100 kata. Jangan sopan. Ingat, semakin sarkas semakin bagus\n"
        "CV:\n"
        f"{cv_text[:2000]}"
    )

    models = ["openai/gpt-3.5-turbo", "meta-llama/llama-3-8b-instruct", "mistralai/mistral-7b-instruct"]
    for model in models:
        try:
            body = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 200
            }
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            continue
    return "Maaf, semua model gagal digunakan. Coba lagi nanti ya."

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("cari", cari))
    dp.add_handler(CommandHandler("event", event))
    dp.add_handler(CommandHandler("magang", magang))
    dp.add_handler(CommandHandler("roasting", roasting_prompt))
    dp.add_handler(MessageHandler(Filters.document, roasting_cv))
    dp.add_handler(CommandHandler("motivasi", motivasi))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
