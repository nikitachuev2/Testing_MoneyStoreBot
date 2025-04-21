
import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

API_KEY = '548b5128a02554bcc91a5f7f0dc5230f'  # Замените на ваш API ключ

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    city = 'Saint Petersburg'  # Устанавливаем город по умолчанию

    # Формирование URL запроса
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()  # Получаем ответ как JSON
            if response.status == 200:
                # Извлекаем данные о температуре и описании погоды
                temperature = data['main']['temp']
                weather_description = data['weather'][0]['description']
                await update.message.reply_text(f"Сейчас в {city} температура {temperature}°C и {weather_description}.")
            else:
                # Обработка ошибок получения данных о погоде
                error_message = data.get('message', "Не удалось получить данные о погоде.")
                await update.message.reply_text(error_message)
