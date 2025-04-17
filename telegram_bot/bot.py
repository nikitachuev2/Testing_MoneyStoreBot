
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from handlers import start, help_command, register, login, add_purchase, analyze_expenses, set_savings_ratio, set_dream, add_salary, show_pocket, show_dream
from auth import register_user, authenticate_user, change_password  # Предполагается, что есть такая функция для смены пароля

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "Привет! Я ваш телеграм бот.\n"
        "Я помогу вам управлять вашим бюджетом и достигать финансовых целей. "
        "Вот некоторые команды, с которыми вы можете взаимодействовать:\n"
    )

    # Кнопки для взаимодействия
    keyboard = [
        ["/register", "/login"],
        ["/add", "/analyze"],
        ["/salary", "/pocket"],
        ["/dream", "/show"],
        ["/help"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Вот список доступных команд:\n"
        "/start - Приветствие\n"
        "/help - Помощь\n"
        "/register - Зарегистрироваться в системе\n"
        "/login - Войти в систему\n"
        "/add - Добавить покупку\n"
        "/analyze - Анализ расходов\n"
        "/salary - Добавить сумму к бюджету\n"
        "/ratio - Установить распределение сбережений\n"
        "/dream - Установить мечту\n"
        "/show - Показать состояние мечты\n"
        "/pocket - Показать остаток на потребление\n"
    )
    
    await update.message.reply_text(help_text)

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Логика добавления покупки
    args = context.args
    if len(args) < 3:
        await update.message.reply_text("Используйте: /add <сумма> <категория>")
        return
    
    sum, category = args[0], args[1]

    # Логика добавления записи в базу данных
    await update.message.reply_text(f"Покупка на сумму {sum} в категории {category} добавлена.")

async def analyze_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Логика для сбора статистики расходов
    await update.message.reply_text("Анализ расходов за месяц... (добавьте функционал)")

async def set_savings_ratio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Логика для настройки процентов сбережений
    await update.message.reply_text("Установите распределение сбережений... (добавьте функционал)")

async def set_dream(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Логика для установки мечты
    await update.message.reply_text("Создайте свою финансовую цель... (добавьте функционал)")

async def add_salary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Логика для добавления дохода
    await update.message.reply_text("Добавьте свою сумму дохода... (добавьте функционал)")

async def show_pocket(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Логика для показа остатка средств
    await update.message.reply_text("Ваш текущий остаток на потребление... (добавьте функционал)")

async def show_dream(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Логика для показа состояния мечты

    await update.message.reply_text("Процент достижения вашей мечты... (добавьте функционал)")

def main():
    application = ApplicationBuilder().token('7969141078:AAFsuZZUxp8QAUNp-Xpf71SAmxQxYzdfKTo').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("analyze", analyze_expenses))
    application.add_handler(CommandHandler("ratio", set_savings_ratio))
    application.add_handler(CommandHandler("dream", set_dream))
    application.add_handler(CommandHandler("salary", add_salary))
    application.add_handler(CommandHandler("pocket", show_pocket))
    application.add_handler(CommandHandler("show", show_dream))
    
    application.run_polling()

if __name__ == '__main__':
    main()
