import random
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

GUESSING = range(1)

# Запуск игры
async def guess_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    number = random.randint(1, 100)
    context.user_data["number"] = number
    await update.message.reply_text("🎯 Я загадал число от 1 до 100. Попробуйте угадать!")
    return GUESSING

# Проверка попытки
async def check_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if "number" not in context.user_data:
        await update.message.reply_text("Начните сначала, используя 'Угадай число'.")
        return ConversationHandler.END

    try:
        guess = int(update.message.text)
        number = context.user_data["number"]

        if guess < number:
            await update.message.reply_text("📉 Слишком маленькое. Попробуйте снова.")
            return GUESSING
        elif guess > number:
            await update.message.reply_text("📈 Слишком большое. Попробуйте снова.")
            return GUESSING
        else:
            await update.message.reply_text("🎉 Поздравляю! Вы угадали число!")
            del context.user_data["number"]
            return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("⚠️ Пожалуйста, введите целое число.")
        return GUESSING