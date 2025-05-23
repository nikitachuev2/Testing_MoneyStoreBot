# Telegram Bot Tests
# Ковалев, P4150
## Установка библиотек
Установите библиотеки, если не установлены
```
pip install pytest pytest-asyncio behave
```
## Запуск unit-тестов
Положить файлы unittests.py и pytest.ini в корневую папку бота и в командной строке:
```
pytest unittests.py
```
## Запуск тестов на естественном языке
Положить папку features в корневую папку бота и в командной строке:
```
behave features/telegram_bot.feature
```