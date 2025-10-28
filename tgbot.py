import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = "8295416672:AAERh0iCC0VqYwpHdJkKSrLLXSy7vxrruZk"  # вставь сюда токен от BotFather

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    try:
        # Папка для временных файлов
        os.makedirs("downloads", exist_ok=True)
        output_path = "downloads/%(title)s.%(ext)s"

        # Настройки yt-dlp
        ydl_opts = {
            "outtmpl": output_path,
            "format": "mp4",
            "quiet": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Отправляем видео пользователю
        await update.message.reply_video(video=open(filename, "rb"))

        # Удаляем файл после отправки
        os.remove(filename)

    except Exception as e:
        print("Ошибка:", e)
        await update.message.reply_text("⚠️ Не удалось скачать видео. Возможно, ссылка не поддерживается.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video))

app.run_polling()

