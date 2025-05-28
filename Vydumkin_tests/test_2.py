
import pytest
from unittest.mock import AsyncMock, patch
from telegram.ext import ConversationHandler
from register import register_start, register_email, register_password, REGISTER_EMAIL, REGISTER_PASSWORD
from roulette_game import roulette, handle_roulette_choice, return_to_main_menu, CHOOSING
import auth

@pytest.mark.asyncio
async def test_register_start():
    update = AsyncMock()
    update.message.reply_text = AsyncMock()
    context = type('Ctx', (), {'user_data': {}})()
    ret = await register_start(update, context)
    update.message.reply_text.assert_awaited_with("Введите свой email для регистрации:")
    assert ret == REGISTER_EMAIL

@pytest.mark.asyncio
async def test_register_email():
    update = AsyncMock()
    update.message.reply_text = AsyncMock()
    context = type('Ctx', (), {'user_data': {}})()
    update.message.text = "test@example.com "
    ret = await register_email(update, context)
    assert context.user_data['email'] == "test@example.com"
    update.message.reply_text.assert_awaited_with("Введите свой пароль:")
    assert ret == REGISTER_PASSWORD

@pytest.mark.asyncio
async def test_register_password_success_fail():
    update = AsyncMock()
    update.message.reply_text = AsyncMock()
    context = type('Ctx', (), {'user_data': {'email': 'e'}})()

    with patch('auth.register_user', return_value=True):
        ret = await register_password(update, context)
        update.message.reply_text.assert_awaited_with("Регистрация прошла успешно!")
        assert ret == ConversationHandler.END

    with patch('auth.register_user', return_value=False):
        ret = await register_password(update, context)
        update.message.reply_text.assert_awaited_with("Ошибка регистрации. Попробуйте снова.")
        assert ret == ConversationHandler.END

@pytest.mark.asyncio
async def test_roulette():
    update = AsyncMock()
    update.message.reply_text = AsyncMock()
    context = type('Ctx', (), {})()
    ret = await roulette(update, context)
    update.message.reply_text.assert_awaited()
    assert ret == CHOOSING

@pytest.mark.asyncio
@patch('random.choice', lambda options: "красное")
async def test_handle_roulette_choice_win():
    update = AsyncMock()
    update.message.reply_text = AsyncMock()
    update.message.text = "Красное"
    ret = await handle_roulette_choice(update, None)
    update.message.reply_text.assert_awaited()
    assert ret == ConversationHandler.END

@pytest.mark.asyncio
@patch('random.choice', lambda options: "черное")
async def test_handle_roulette_choice_lose():
    update = AsyncMock()
    update.message.reply_text = AsyncMock()
    update.message.text = "Красное"
    ret = await handle_roulette_choice(update, None)
    update.message.reply_text.assert_awaited()
    assert ret == ConversationHandler.END

@pytest.mark.asyncio
async def test_handle_roulette_choice_invalid():
    update = AsyncMock()
    update.message.reply_text = AsyncMock()
    update.message.text = "Зелёное"
    ret = await handle_roulette_choice(update, None)
    update.message.reply_text.assert_awaited_with("⚠️ Пожалуйста, выберите 'Красное' или 'Черное'.")
    assert ret == CHOOSING

@pytest.mark.asyncio
async def test_return_to_main_menu():
    update = AsyncMock()
    update.message.reply_text = AsyncMock()
    await return_to_main_menu(update, None)
    update.message.reply_text.assert_awaited()
