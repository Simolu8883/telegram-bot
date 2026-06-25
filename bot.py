from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
from langdetect import detect
import os
import asyncio

TOKEN = os.getenv("TOKEN")

TARGET_LANG = "it"

async def translate_text(text):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: GoogleTranslator(source='auto', target=TARGET_LANG).translate(text)
    )

async def translate_forwarded(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message

    if not msg:
        return

    # ✅ SOLO inoltri
    if not msg.forward_date:
        return

    # ✅ testo o caption
    text = msg.text or msg.caption
    if not text:
        return

    try:
        # ✅ detect lingua
        lang = detect(text)

        # ✅ IGNORA italiano
        if lang == "it":
            return

        translated = await translate_text(text)

        await msg.reply_text(translated)

    except Exception as e:
        print(f"Errore: {e}")


app = ApplicationBuilder().token(TOKEN).build()

# ✅ filtro più preciso (no filters.ALL)
app.add_handler(MessageHandler(filters.TEXT | filters.Caption(True), translate_forwarded))

print("✅ Bot versione finale attivo")
app.run_polling()
