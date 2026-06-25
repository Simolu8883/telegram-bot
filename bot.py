
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
import os

TOKEN = os.getenv("TOKEN")

TARGET_LANG = "it"

async def translate_all(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message

    if not msg:
        return

    # ✅ prende testo O caption (foto/video)
    text = msg.text if msg.text else msg.caption

    if not text:
        return

    try:
        translated = GoogleTranslator(
            source='auto',
            target=TARGET_LANG
        ).translate(text)

        await msg.reply_text(translated)

    except Exception as e:
        print(f"Errore: {e}")


app = ApplicationBuilder().token(TOKEN).build()

# ✅ IMPORTANTISSIMO → intercetta tutto
app.add_handler(MessageHandler(filters.ALL, translate_all))

print("✅ Bot completo attivo")
app.run_polling()
