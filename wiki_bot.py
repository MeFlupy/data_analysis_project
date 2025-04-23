from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import wikipedia

wikipedia.set_lang("ru")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши термин, и я найду его определение на Википедии 📚")

async def get_definition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    term = update.message.text
    try:
        summary = wikipedia.summary(term, sentences=3)
        await update.message.reply_text(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        options = '\n'.join(e.options[:5])
        await update.message.reply_text(f"🔍 Слишком много значений. Уточни термин:\n{options}")
    except wikipedia.exceptions.PageError:
        await update.message.reply_text("❌ Термин не найден. Попробуй другой.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

def main():
    TOKEN = "7726127832:AAGrX9aAJ_EC_5jY6a79nASZATLaDySHtn4"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_definition))

    print("✅ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
