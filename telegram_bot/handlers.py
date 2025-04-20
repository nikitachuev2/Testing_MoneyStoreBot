
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (ContextTypes, CommandHandler, MessageHandler, filters)
import random  # Импортируем модуль random для выбора результата

import login
import register
from current_datetime import current_datetime
from random_fact import random_fact
from guess_number import guess_number, check_number  # Убедитесь, что эти функции правильно определены в guess_number.py
from weather import show_weather  # Импортируем функцию для показа погоды
from spending_advice import spending_advice  # Импортируем функцию советов по тратам

# Обработчик для русской рулетки, который предлагает кнопку выбора
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

# Обработка выбора пользователя
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "Привет! Я ваш телеграм бот.\n"
        "Я помогу вам управлять вашим бюджетом и достигать финансовых целей. "
        "Вот некоторые команды, с которыми вы можете взаимодействовать:\n"
    )

    keyboard = [
        ["Регистрация", "Вход"],
        ["Добавить покупку", "Анализ расходов", "Добавить сумму к бюджету"],
        ["Справка", "Текущая дата и время"],
        ["Случайный факт", "Угадай число"],
        ["Показать погоду", "Русская рулетка", "Совет потратить"]  # Добавили новые кнопки
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
        "/add - добавление покупки\n"
        "/datetime - показать текущую дату и время\n"
        "/fact - случайный факт\n"
        "/guess - начать игру 'угадай число'\n"
        "/weather - показать погоду\n"  # Добавили команду для погоды
        "/roulette - русская рулетка\n"  # Добавили команду для русской рулетки

        "/advice - совет по тратам\n"  # Добавили команду для совета по тратам
    )
    await update.message.reply_text(help_text)

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Используйте: /add <сумма> <категория>")
        return
    sum = args[0]
    category = args[1]
    await update.message.reply_text(f"Покупка на сумму {sum} в категории {category} добавлена.")

async def analyze_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Анализ расходов за месяц... (добавьте функционал)")

async def set_savings_ratio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Установите распределение сбережений... (добавьте функционал)")

async def set_dream(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Создайте свою финансовую цель... (добавьте функционал)")

async def add_salary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Добавьте свою сумму дохода... (добавьте функционал)")

async def show_pocket(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Ваш текущий остаток на потребление... (добавьте функционал)")

async def show_dream(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Процент достижения вашей мечты... (добавьте функционал)")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    if text == "Регистрация":
        await register.register_start(update, context)
    elif text == "Вход":
        await login.login_start(update, context)
    elif text == "Справка":
        await help_command(update, context)
    elif text == "Добавить покупку":
        await add(update, context)
    elif text == "Анализ расходов":
        await analyze_expenses(update, context)
    elif text == "Добавить сумму к бюджету":
        await add_salary(update, context)
    elif text == "Русская рулетка":
        await russian_roulette(update, context)  # Новый вызов для рулетки
    elif text in ["Красное", "Черное"]:  # Определяем, если был выбран один из вариантов
        await handle_roulette_choice(update, context)  # Обработка выбора

# Регистрация обработчиков
def register_handlers(application):
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('roulette', russian_roulette))  # Команда запуска рулетки
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))  # Обработка выбора пользователем
