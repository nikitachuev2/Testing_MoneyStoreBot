
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (ContextTypes, ConversationHandler,
                            CommandHandler, MessageHandler, filters)
import login
import register
from current_datetime import current_datetime  # Импортируем функцию
from guess_number import guess_number  # Импортируем функцию
from random_fact import random_fact  # Импортируем функцию
from roulette import roulette  # Импортируем функцию
from roulette import handle_roulette_choice  # Импортируем функцию, которую не было
from spending_advice import spending_advice  # Импортируем функцию
from weather import weather  # Импортируем функцию

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "✨ Приветствую! Я ваш волшебный телеграм бот. ✨\n"
        "Здесь вы найдете множество увлекательных и полезных функций для развлечения и получения информации.\n"
        "Давайте начинать! Вот что я умею:\n"
    )

    keyboard = [
        ["Регистрация", "Вход"],
        ["Справка", "Текущая дата и время"],
        ["Угадай число", "Случайный факт"],
        ["Русская рулетка", "Денежный совет"],
        ["Погода"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Вот список доступных команд:\n"
        "/start - приветствие\n"
        "/help - список команд\n"
        "/register - регистрация пользователя\n"
        "/login - вход в аккаунт\n"
        "/current_datetime - показать текущую дату и время\n"
        "/guess_number - сыграть в угадай число\n"
        "/random_fact - получить случайный факт\n"
        "/roulette - сыграть в русскую рулетку\n"
        "/spending_advice - получить денежный совет\n"
        "/weather - узнать погоду\n"
    )
    await update.message.reply_text(help_text)



async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    if text == "Регистрация":
        return await register.register_start(update, context)
    elif text == "Вход":
        return await login.login_start(update, context)
    elif text == "Справка":
        return await help_command(update, context)
    elif text == "Текущая дата и время":
        return await current_datetime(update, context)
    elif text == "Угадай число":
        return await guess_number(update, context)
    elif text == "Случайный факт":
        return await random_fact(update, context)
    elif text == "Русская рулетка":
        return await roulette(update, context)
    elif text == "Денежный совет":
        return await spending_advice(update, context)
    elif text == "Погода":
        return await weather(update, context)  # Исправлено: вызов правильной функции для погоды.


# Конфигурация обработчиков для регистрации
conv_handler_register = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler)],
    states={
        register.REGISTER_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, register.register_email)],
        register.REGISTER_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, register.register_password)],
    },
    fallbacks=[],
)

# Конфигурация обработчиков для входа
conv_handler_login = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler)],
    states={
        login.LOGIN_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, login.login_email)],
        login.LOGIN_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, login.login_password)],
    },
    fallbacks=[],
)

def register_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler_register)
    application.add_handler(conv_handler_login)

    # Добавляем обработчик для основных кнопок
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

CHOOSING = range(1)

conv_handler_roulette = ConversationHandler(
    entry_points=[CommandHandler('roulette', roulette)],
    states={
        CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_roulette_choice)],
    },
    fallbacks=[],
)

# Вставьте это в вашу функцию `register_handlers`
def register_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler_register)
    application.add_handler(conv_handler_login)
    application.add_handler(conv_handler_roulette)
