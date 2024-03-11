# bot.py
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from .config import telegram_token
from .handlers import start, help_command, process_message

application = Application.builder().token(telegram_token).build()

def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

def main():
    setup_handlers(application)
    application.run_polling()

if __name__ == "__main__":
    main()
