
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN
from handlers import start, help_command  # Здесь вы импортируете нужные обработчики

# Основная асинхронная функция
async def main():
    # Создаем приложение
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    # Запуск бота
    await app.run_polling()

# Убедитесь, что вы правильно используете "__name__" и "__main__"
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
