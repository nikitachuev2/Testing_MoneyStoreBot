
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters
from auth import register_user, authenticate_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "Привет! Я ваш телеграм бот.\n"
        "Я помогу вам управлять вашим бюджетом и достигать финансовых целей. "
        "Вот некоторые команды, с которыми вы можете взаимодействовать:\n"
    )

    # Кнопки для взаимодействия
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
        "/analyze - анализ расходов\n"
        "/salary - добавление суммы к бюджету\n"
        "/ratio - установка распределения сбережений\n"
        "/dream - установка мечты\n"
        "/show - показать процент достижения мечты\n"
        "/pocket - показать текущий остаток на потребление\n"
    )
    await update.message.reply_text(help_text)

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text("Пожалуйста, укажите email и пароль.\nИспользуйте команду так: /register [email] [password]")
        return
    email, password = context.args[0], context.args[1]
    try:
        register_user(email, password)
        await update.message.reply_text("Регистрация успешна! Вы можете войти с помощью /login.")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка при регистрации: {str(e)}")

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text("Пожалуйста, укажите email и пароль.\nИспользуйте команду так: /login [email] [password]")
        return
    email, password = context.args[0], context.args[1]
    if authenticate_user(email, password):
        await update.message.reply_text("Вход успешен! Добро пожаловать.")
    else:
        await update.message.reply_text("Ошибка: Неправильный email или пароль.")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Используйте: /add <сумма> <категория>")
        return
    
    sum, category = args[0], args[1]
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
    if text == "/register":
        await register(update, context)
    elif text == "/login":
        await login(update, context)
    elif text == "/help":
        await help_command(update, context)
    elif text == "/add":
        await add(update, context)
    elif text == "/analyze":
        await analyze_expenses(update, context)
    elif text == "/salary":
        await add_salary(update, context)
    elif text == "/ratio":
        await set_savings_ratio(update, context)
    elif text == "/dream":
        await set_dream(update, context)
    elif text == "/show":
        await show_dream(update, context)
    elif text == "/pocket":
        await show_pocket(update, context)
    else:
        await update.message.reply_text("Неизвестная команда. Пожалуйста, используйте /help для получения информации.")

def main():
    application = ApplicationBuilder().token('YOUR_TELEGRAM_BOT_TOKEN').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("analyze", analyze_expenses))
    application.add_handler(CommandHandler("salary", add_salary))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
