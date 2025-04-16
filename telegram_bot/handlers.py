
from telegram import Update
from telegram.ext import ContextTypes
from auth import register_user, authenticate_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "Привет! Я ваш телеграм бот.\n"
        "Я помогу вам управлять вашим бюджетом и достигать финансовых целей. "
        "Вот некоторые команды, с которыми вы можете взаимодействовать:\n"
        "/start - Приветственное сообщение\n"
        "/help - Список всех доступных команд\n"
        "/register - Регистрация нового пользователя\n"
        "/login - Вход в систему\n"
        "/add - Добавить покупку\n"
        "/analyze - Анализ расходов\n"
        "/salary - Добавить сумму к бюджету\n"
        "/ratio - Установить распределение сбережений\n"
        "/dream - Установить мечту\n"
        "/show - Показать состояние мечты\n"
        "/pocket - Показать остаток на потребление\n"
    )
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
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
    try:
        email, password = context.args
        register_user(email, password)
        await update.message.reply_text("Регистрация успешна! Вы можете войти с помощью /login.")
    except ValueError:
        await update.message.reply_text("Используйте команду так: /register [email] [password]")

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        email, password = context.args
        if authenticate_user(email, password):
            await update.message.reply_text("Вход успешен! Добро пожаловать.")
        else:
            await update.message.reply_text("Ошибка: Неправильный email или пароль.")
    except ValueError:
        await update.message.reply_text("Используйте команду так: /login [email] [password]")
