
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from handlers import start, help_command, register, login
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

def main():
    application = ApplicationBuilder().token('7969141078:AAFsuZZUxp8QAUNp-Xpf71SAmxQxYzdfKTo').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("login", login))
    
    application.run_polling()

if __name__ == '__main__':
    main()
