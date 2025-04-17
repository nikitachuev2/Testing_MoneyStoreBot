from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler)
from database import create_tables
from handlers import register_handlers
def main():
    application = ApplicationBuilder().token('7969141078:AAFsuZZUxp8QAUNp-Xpf71SAmxQxYzdfKTo').build()
    create_tables()
    register_handlers(application)
    application.run_polling()

if __name__ == '__main__':
    main()
