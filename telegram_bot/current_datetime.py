from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
async def current_datetime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    now = datetime.now()  # Получаем текущее время
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Форматируем его
    await update.message.reply_text(f'Текущая дата и время: {current_time}')  # Асинхронный ответ
