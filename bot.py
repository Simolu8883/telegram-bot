
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
from langdetect import detect
import os

TOKEN = os.getenv("TOKEN")
TARGET_LANG = "it"

async def translate_forwarded(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if message.forward_origin and message.text:
        original_text = message.text

        try:
            lang = detect(original_text)

            if lang != TARGET_LANG:
                translated = GoogleTranslator(source='auto', target=TARGET_LANG).translate(original_text)
                await message.reply_text(f"🌐 Traduzione:\n{translated}")

        except Exception as e:
            print(e)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), translate_forwarded))

app.run_polling()
