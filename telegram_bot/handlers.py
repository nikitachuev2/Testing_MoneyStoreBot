from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

import login
import register
from current_datetime import current_datetime
from guess_number import guess_number, check_number
from random_fact import random_fact
from roulette import roulette, handle_roulette_choice, CHOOSING
from spending_advice import spending_advice
from weather import weather

# Состояния для угадайки
GUESSING = range(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["Регистрация", "Вход"],
        ["Справка", "Текущая дата и время"],
        ["Угадай число", "Случайный факт"],
        ["Русская рулетка", "Денежный совет"],
        ["Погода"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    welcome_text = (
        "✨ Привет! Я волшебный бот. Вот, что я умею:\n"
        "- Регистрация/Вход\n"
        "- Угадай число\n"
        "- Русская рулетка\n"
        "- И многое другое..."
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Список команд:\n"
        "/start — начать\n"
        "/help — справка\n"
        "/guess_number — угадай число\n"
        "/roulette — русская рулетка\n"
    )

# Главный обработчик кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
        await guess_number(update, context)
        return GUESSING
    elif text == "Случайный факт":
        return await random_fact(update, context)
    elif text == "Русская рулетка":
        return await roulette(update, context)
    elif text == "Денежный совет":
        return await spending_advice(update, context)
    elif text == "Погода":
        return await weather(update, context)

# РЕГИСТРАЦИЯ — ConversationHandler
conv_handler_register = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Регистрация$"), register.register_start)],
    states={
        register.REGISTER_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, register.register_email)],
        register.REGISTER_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, register.register_password)],
    },
    fallbacks=[],
)

# ВХОД — ConversationHandler
conv_handler_login = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Вход$"), login.login_start)],
    states={
        login.LOGIN_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, login.login_email)],
        login.LOGIN_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, login.login_password)],
    },
    fallbacks=[],
)

# РУЛЕТКА — ConversationHandler
conv_handler_roulette = ConversationHandler(
    entry_points=[
        CommandHandler("roulette", roulette),
        MessageHandler(filters.Regex("^Русская рулетка$"), roulette),
    ],
    states={
        CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_roulette_choice)],
    },
    fallbacks=[],
)

# УГАДАЙ ЧИСЛО — ConversationHandler
conv_handler_guess = ConversationHandler(
    entry_points=[
        CommandHandler("guess_number", guess_number),
        MessageHandler(filters.Regex("^Угадай число$"), guess_number),
    ],
    states={
        GUESSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_number)],
    },
    fallbacks=[],
)

# Финальная регистрация обработчиков
def register_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(conv_handler_register)
    application.add_handler(conv_handler_login)
    application.add_handler(conv_handler_roulette)
    application.add_handler(conv_handler_guess)

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))