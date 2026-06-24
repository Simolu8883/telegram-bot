from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
from langdetect import detect
import os

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN mancante!")

# ✅ CONFIG
TARGET_LANG = "it"
ALLOWED_USER_ID = None  # inserisci il tuo ID se vuoi limitare

async def translate_forwarded(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message

    # ✅ solo inoltri con testo
    if not msg or not msg.forward_origin or not msg.text:
        return

    text = msg.text

    try:
        detected = detect(text)

        # ✅ evita traduzione inutile
        if detected == TARGET_LANG:
            return

        translated = GoogleTranslator(
            source='auto',
            target=TARGET_LANG
        ).translate(text)

        # ✅ SOLO traduzione (pulito)
        await msg.reply_text(translated)

    except Exception as e:
        print(f"Errore: {e}")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), translate_forwarded))

print("✅ Bot pulito attivo")
app.run_polling()
