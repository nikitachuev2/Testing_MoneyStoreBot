from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (ContextTypes, ConversationHandler,
                            CommandHandler, MessageHandler, filters)
import auth
LOGIN_EMAIL, LOGIN_PASSWORD = range(2, 4)
async def login_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Введите свой email для входа:")
    return LOGIN_EMAIL  # Переходим к этапу EMAIL

async def login_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['email'] = update.message.text.strip()  # Убираем пробелы
    await update.message.reply_text("Введите свой пароль:")
    return LOGIN_PASSWORD  # Переходим к этапу PASSWORD

async def login_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    email = context.user_data['email']
    password = update.message.text.strip()  # Убираем пробелы
    if auth.authenticate_user(email, password):  # Проверяем вход
        await update.message.reply_text("Вход успешен! Добро пожаловать!")
    else:
        await update.message.reply_text("Ошибка входа. Проверьте email и пароль.")
    return ConversationHandler.END  # Завершаем конверсацию

