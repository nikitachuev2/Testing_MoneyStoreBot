
import pytest
from unittest.mock import AsyncMock
from telegram.ext import ConversationHandler
from current_datetime import current_datetime
from guess_number import guess_number, check_number, GUESSING
from login import login_start, login_email, login_password
from random_fact import random_fact

pytestmark = pytest.mark.asyncio

class DummyMessage:
    def __init__(self, text=None):
        self.text = text
        self.reply_text = AsyncMock()

class DummyUpdate:
    def __init__(self, text=None):
        self.message = DummyMessage(text=text)

class DummyContext:
    def __init__(self):
        self.user_data = {}

async def test_current_datetime_sends_message():
    update = DummyUpdate()
    context = DummyContext()
    await current_datetime(update, context)
    assert update.message.reply_text.called
    msg = update.message.reply_text.call_args[0][0]
    assert msg.startswith('Текущая дата и время:')

async def test_guess_number_starts_game():
    update = DummyUpdate()
    context = DummyContext()
    ret = await guess_number(update, context)
    assert ret == GUESSING
    assert "number" in context.user_data
    assert 1 <= context.user_data["number"] <= 100
    update.message.reply_text.assert_called_once()

async def test_check_number_correct_guess():
    update = DummyUpdate(text='50')
    context = DummyContext()
    context.user_data["number"] = 50
    ret = await check_number(update, context)
    update.message.reply_text.assert_awaited_with("🎉 Поздравляю! Вы угадали число!")
    assert ret == ConversationHandler.END
    assert "number" not in context.user_data

async def test_check_number_number_missing():
    update = DummyUpdate(text='10')
    context = DummyContext()
    ret = await check_number(update, context)
    update.message.reply_text.assert_awaited_with("Начните сначала, используя 'Угадай число'.")
    assert ret == ConversationHandler.END

async def test_check_number_too_low():
    update = DummyUpdate(text='10')
    context = DummyContext()
    context.user_data["number"] = 20
    ret = await check_number(update, context)
    update.message.reply_text.assert_awaited_with("📉 Слишком маленькое. Попробуйте снова.")
    assert ret == GUESSING

async def test_check_number_too_high():
    update = DummyUpdate(text='30')
    context = DummyContext()
    context.user_data["number"] = 20
    ret = await check_number(update, context)
    update.message.reply_text.assert_awaited_with("📈 Слишком большое. Попробуйте снова.")
    assert ret == GUESSING

async def test_check_number_invalid_input():
    update = DummyUpdate(text='abc')
    context = DummyContext()
    context.user_data["number"] = 20
    ret = await check_number(update, context)
    update.message.reply_text.assert_awaited_with("⚠️ Пожалуйста, введите целое число.")
    assert ret == GUESSING

async def test_login_start_sends_prompt():
    update = DummyUpdate()
    context = DummyContext()
    ret = await login_start(update, context)
    update.message.reply_text.assert_awaited_with("Введите свой email для входа:")
    assert ret == 2

async def test_login_email_saves_email():
    update = DummyUpdate(text=" test@example.com ")
    context = DummyContext()
    ret = await login_email(update, context)
    assert context.user_data['email'] == "test@example.com"
    update.message.reply_text.assert_awaited_with("Введите свой пароль:")
    assert ret == 3

async def test_login_password_authentication(monkeypatch):
    update = DummyUpdate(text="password123")
    context = DummyContext()
    context.user_data['email'] = "test@example.com"
    import login
    def fake_authenticate_user_success(email, password):
        return True

    def fake_authenticate_user_fail(email, password):
        return False
    monkeypatch.setattr(login.auth, "authenticate_user", fake_authenticate_user_success)
    ret = await login_password(update, context)
    update.message.reply_text.assert_awaited_with("Вход успешен! Добро пожаловать!")
    assert ret == ConversationHandler.END
    monkeypatch.setattr(login.auth, "authenticate_user", fake_authenticate_user_fail)
    ret = await login_password(update, context)
    update.message.reply_text.assert_awaited_with("Ошибка входа. Проверьте email и пароль.")
    assert ret == ConversationHandler.END

async def test_random_fact_sends_fact():
    update = DummyUpdate()
    context = DummyContext()
    await random_fact(update, context)
    update.message.reply_text.assert_called_once()
    msg = update.message.reply_text.call_args[0][0]
    assert msg.startswith("Здесь интересный факт: ")
