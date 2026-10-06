import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from groq import Groq
TOKEN=os.environ.get("TOKEN")
GROQ_KEY=os.environ.get("GROQ_API_KEY")
client=Groq(api_key=GROQ_KEY)
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أنا بوت تفريغ الصوتيات السوري 🇸🇾\n🎙️ أرسل فويس")
async def handle(update:Update,context:ContextTypes.DEFAULT_TYPE):
    try:
        f=await context.bot.get_file(update.message.voice or update.message.audio or update.message.video or update.message.document)
        await f.download_to_drive("temp.ogg")
        await update.message.reply_text("⏳ ثواني وبيجهز...")
        with open("temp.ogg","rb") as file:
            text=client.audio.transcriptions.create(file=("temp.ogg",file.read()),model="whisper-large-v3",language="ar",response_format="text")
        await update.message.reply_text(str(text))
        os.remove("temp.ogg")
    except Exception as e:
        await update.message.reply_text(f"خطأ: {e}")
app=Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO | filters.VIDEO | filters.Document.ALL,handle))
print("Bot running...")
app.run_polling()
