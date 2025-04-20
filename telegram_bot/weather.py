
import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'  # Замените на ваш API ключ

async def show_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    city = 'Moscow'  # Здесь можно заменить на любой другой город
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if response.status == 200:
                temperature = data['main']['temp']
                weather_description = data['weather'][0]['description']
                await update.message.reply_text(f"Сейчас в {city} температура {temperature}°C и {weather_description}.")
            else:
                await update.message.reply_text("Не удалось получить данные о погоде.")

