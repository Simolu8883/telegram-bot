
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
from langdetect import detect
import os

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN mancante!")

# ✅ CONFIG
TARGET_LANG = "it"   # lingua finale (it, en, fr, de, es...)
ALLOWED_USER_ID = None  # inserisci il tuo user ID Telegram per limitare

# 🔍 funzione principale
async def translate_forwarded(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message

    if not message:
        return

    # ✅ SOLO messaggi inoltrati
    if not message.forward_origin:
        return

    # ✅ SOLO testo
    if not message.text:
        return

    text = message.text

    try:
        detected_lang = detect(text)

        # ✅ evita traduzione inutile
        if detected_lang == TARGET_LANG:
            return

        translated = GoogleTranslator(
            source='auto',
            target=TARGET_LANG
        ).translate(text)

        # ✅ formato migliorato
        reply = f"🌐 Traduzione:\n{translated}"

        await message.reply_text(reply)

    except Exception as e:
        print(f"Errore: {e}")


# ✅ avvio bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), translate_forwarded))

print("✅ Bot avviato")
app.run_polling()
