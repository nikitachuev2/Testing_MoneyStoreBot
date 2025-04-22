
import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

CHOOSING = range(1)

# Запуск игры
async def roulette(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [["Красное", "Черное"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🎲 Рулетка запущена! Выберите 'Красное' или 'Черное':",
        reply_markup=reply_markup
    )

    return CHOOSING

# Обработка выбора
async def handle_roulette_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip().lower()

    if user_choice not in ["красное", "черное"]:
        await update.message.reply_text("⚠️ Пожалуйста, выберите 'Красное' или 'Черное'.")
        return CHOOSING

    outcome = random.choice(["красное", "черное"])

    if user_choice == outcome:
        result = f"✅ Вы выбрали {user_choice}. Поздравляем, вы выиграли! Это было {outcome}!"
    else:
        result = f"❌ Вы выбрали {user_choice}. Увы, вы проиграли. Это было {outcome}."

    await update.message.reply_text(result, reply_markup=ReplyKeyboardRemove())
    
    # Заканчиваем разговор и создаем кнопку для возврата в главное меню
    await return_to_main_menu(update, context)

    return ConversationHandler.END

# Функция для возврата в главное меню
async def return_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["Регистрация", "Вход"],
        ["Справка", "Текущая дата и время"],
        ["Угадай число", "Случайный факт"],
        ["Русская рулетка", "Денежный совет"],
        ["Погода"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "🔙 Произошел возврат в меню. Выберитке функцию при помощи кнопок",
        reply_markup=reply_markup
    )
