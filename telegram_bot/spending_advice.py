
import random
from telegram import Update
from telegram.ext import ContextTypes

spending_tips = [
    "Сделайте небольшие сбережения на незапланированный случай.",
    "Не тратьте все деньги на развлечения. Попробуйте бюджетные варианты.",
    "Сравните цены на необходимые вещи, прежде чем совершать покупку.",
    "Инвестируйте в свое образование — это самый надежный способ потратить деньги.",
    "Покупая что-то новое, подумайте, как долго это вам послужит."
]

async def spending_advice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    advice = random.choice(spending_tips)
    await update.message.reply_text(f"Совет: {advice}")
