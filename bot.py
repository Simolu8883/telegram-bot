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

    # ✅ SOLO inoltri (metodo stabile)
    if not msg.forward_date:
        return

    # ✅ testo o caption
    text = msg.text or msg.caption
    if not text:
        return

    try:
        # ✅ prova a rilevare lingua
        try:
            lang = detect(text)
        except:
            lang = "unknown"

        # ✅ IGNORA SOLO italiano (robusto)
        if lang.startswith("it"):
            return

        translated = await translate_text(text)

        # ✅ evita doppioni (fallback sicurezza)
        if translated.strip().lower() == text.strip().lower():
            return

        await msg.reply_text(translated)

    except Exception as e:
        print(f"Errore: {e}")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT | filters.Caption(True), translate_forwarded))

print("✅ Bot finale stabile attivo")
app.run_polling()
