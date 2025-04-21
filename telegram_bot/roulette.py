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
    return ConversationHandler.END