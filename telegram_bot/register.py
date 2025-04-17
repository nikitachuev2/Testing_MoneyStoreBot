from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (ContextTypes, ConversationHandler,
                            CommandHandler, MessageHandler, filters)
import auth
REGISTER_EMAIL, REGISTER_PASSWORD = range(2)
# Начало регистрации
async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Введите свой email для регистрации:")
    return REGISTER_EMAIL  # Переходим к этапу EMAIL

async def register_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['email'] = update.message.text.strip()  # Убираем пробелы
    await update.message.reply_text("Введите свой пароль:")
    return REGISTER_PASSWORD# Переходим к этапу PASSWORD

async def register_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    email = context.user_data['email']
    password = update.message.text.strip()  # Убираем пробелы
    if auth.register_user(email, password):  # Проверяем регистрацию
        await update.message.reply_text("Регистрация прошла успешно!")
    else:
        await update.message.reply_text("Ошибка регистрации. Попробуйте снова.")
    return ConversationHandler.END  # Завершаем конверсацию

