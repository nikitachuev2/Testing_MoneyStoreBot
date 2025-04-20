
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, Application

async def russian_roulette(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Отправим пользователю сообщение с вариантами выбора
    keyboard = [
        ["Красное", "Черное"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Выберите 'Красное' или 'Черное'.", 
        reply_markup=reply_markup
    )

async def handle_roulette_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_choice = update.message.text.lower()  # Сохраним выбор пользователя
    if user_choice not in ['красное', 'черное']:
        await update.message.reply_text("Выберите либо 'красное', либо 'черное'.")
        return

    outcome = random.choice(['красное', 'черное'])  # Случайный выбор результата
    if user_choice == outcome:
        await update.message.reply_text(f"Вы выбрали {user_choice}. Поздравляем, вы выиграли!")
    else:
        await update.message.reply_text(f"Вы выбрали {user_choice}. К сожалению, вы проиграли. Это {outcome}.")

# Регистрация обработчиков
def register_handlers(application: Application):
    application.add_handler(CommandHandler('roulette', russian_roulette))  # Команда запуска рулетки
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_roulette_choice))  # Обработка выбора пользователем

# Основная функция запуска бота
if __name__ == '__main__':
    application = Application.builder().token('YOUR_TOKEN_HERE').build()  # Замените 'YOUR_TOKEN_HERE' на токен вашего бота
    register_handlers(application)
    application.run_polling()
