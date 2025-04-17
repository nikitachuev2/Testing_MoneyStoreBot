from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (ContextTypes, ConversationHandler,
                            CommandHandler, MessageHandler, filters)
import login
import register
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "Привет! Я ваш телеграм бот.\n"
        "Я помогу вам управлять вашим бюджетом и достигать финансовых целей. "
        "Вот некоторые команды, с которыми вы можете взаимодействовать:\n"
    )

    keyboard = [
        ["Регистрация", "Вход"],
        ["Добавить покупку", "Анализ расходов", "Добавить сумму к бюджету"],
        ["Справка"]
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
        return await register.register_start(update, context)  # Верно
    elif text == "Вход":
        return await login.login_start(update, context)  # Верно
    elif text == "Справка":
        return await help_command(update, context)
    elif text == "Добавить покупку":
        return await add(update, context)
    elif text == "Анализ расходов":
        return await analyze_expenses(update, context)
    elif text == "Добавить сумму к бюджету":
        return await add_salary(update, context)
    elif text == "Соотношение":
        return await set_savings_ratio(update, context)
    elif text == "Мечта":
        return await set_dream(update, context)
    elif text == "Показать":
        return await show_dream(update, context)
    elif text == "Карманные расходы ":
        return await show_pocket(update, context)

conv_handler_register = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler)],
    states={
        register.REGISTER_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, register.register_email)],
        register.REGISTER_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, register.register_password)],
    },
    fallbacks=[],
)

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
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(conv_handler_login)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

