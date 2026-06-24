from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
import os

TOKEN = os.getenv("TOKEN")

TARGET_LANG = "it"
ALLOWED_USER_ID = None

async def translate_forwarded(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message

    if not msg or not msg.text:
        return

    if ALLOWED_USER_ID and msg.from_user.id != ALLOWED_USER_ID:
        return

    text = msg.text

    try:
        translated = GoogleTranslator(
            source='auto',
            target=TARGET_LANG
        ).translate(text)

        await msg.reply_text(translated)

    except Exception as e:
        print(f"Errore: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), translate_forwarded))

print("✅ Bot OK")
app.run_polling()
