
import random
from telegram import Update
from telegram.ext import ContextTypes

# Список фактов
facts = [
    "Факт 1: Медузы состоят на 95% из воды.",
    "Факт 2: Осьминоги имеют три сердца.",
    "Факт 3: Панды могут есть мясо, но в основном предпочитают бамбук.",
    "Факт 4: Луна удаляется от Земли на 3.8 см каждый год.",
    "Факт 5: Сердце кролика бьется примерно 300 раз в минуту."
]

async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    fact = random.choice(facts)  # Случайный выбор факта
    await update.message.reply_text(f'Здесь интересный факт: {fact}')  # Асинхронный ответ
