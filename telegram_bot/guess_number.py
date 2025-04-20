
import random
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

# Функция для начала игры
async def guess_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    number = random.randint(1, 100)  # Генерируем случайное число
    context.user_data['number'] = number  # Сохраняем его в user_data
    await update.message.reply_text('Я загадал число от 1 до 100. Попробуй угадать его!')  # Асинхронный ответ

# Функция для проверки числа
async def check_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'number' in context.user_data:  # Проверяем, есть ли загаданное число
        number = context.user_data['number']
        try:
            guess = int(update.message.text)  # Пробуем преобразовать текст сообщения в число
            if guess < number:
                await update.message.reply_text('Слишком маленькое число. Попробуйте еще раз!')  # Асинхронный ответ
            elif guess > number:
                await update.message.reply_text('Слишком большое число. Попробуйте еще раз!')  # Асинхронный ответ
            else:
                await update.message.reply_text('Поздравляю! Вы угадали число! 🎉')  # Асинхронный ответ
                del context.user_data['number']  # Удаляем загаданное число
        except ValueError:
            await update.message.reply_text('Пожалуйста, введите число.')  # Асинхронный ответ

# Регистрация обработчиков
def register_handlers(application):
    # Обработчик для начала игры
    application.add_handler(CommandHandler('guess', guess_number))
    # Обработчик для проверки числа
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_number))
