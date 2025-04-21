
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
)

# Состояния для рулетки
CHOOSING = range(1)

# Функция, которая запускает игру в рулетку
async def roulette(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Создаем клавиатуру с вариантами выбора
    keyboard = [
        ["Красное", "Черное"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Отправляем сообщение пользователю с запросом выбора
    await update.message.reply_text(
        "Выберите 'Красное' или 'Черное'.", 
        reply_markup=reply_markup
    )
    
    return CHOOSING  # Переход к состоянию выбора

# Функция, которая обрабатывает выбор пользователя
async def handle_roulette_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip().lower()  # Удаляем лишние пробелы и переводим в нижний регистр

    # Проверяем, является ли выбор пользователя допустимым
    if user_choice not in ['красное', 'черное']:
        await update.message.reply_text("Выберите либо 'Красное', либо 'Черное'.")
        return CHOOSING  # Остаемся в состоянии выбора

    # Генерация результата рулетки
    outcome = random.choice(['красное', 'черное'])

    # Проверяем, выиграл ли пользователь
    if user_choice == outcome:
        await update.message.reply_text(f"Вы выбрали {user_choice}. Поздравляем, вы выиграли! Это {outcome}.")
    else:
        await update.message.reply_text(f"Вы выбрали {user_choice}. К сожалению, вы проиграли. Это {outcome}.")

    return ConversationHandler.END  # Завершаем разговор
