
from telegram import Update
from telegram.ext import ContextTypes  # Не забудьте импортировать этот тип

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Я ваш помощник по финансовому планированию...")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands_text = ("Доступные команды:\n"
                     "/start - Приветствие\n"
                     "/help - Список команд")
    await update.message.reply_text(commands_text)
