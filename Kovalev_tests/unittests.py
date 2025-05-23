
import pytest
import sqlite3
import bcrypt
from unittest.mock import patch, MagicMock, AsyncMock
import random
from random_fact import random_fact
from spending_advice import spending_advice
from roulette import handle_roulette_choice
from guess_number import check_number
from weather import weather
from auth import register_user, authenticate_user

@pytest.fixture
def mock_conn_cursor():
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor

def test_register_user_success(mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_cursor.fetchone.return_value = None
    with patch("auth.create_connection", return_value=mock_conn):
        result = register_user("test@example.com", "securepass")
        assert result is True
        assert mock_cursor.execute.call_count == 2
        mock_conn.commit.assert_called_once()

def test_register_user_existing_email(mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_cursor.fetchone.return_value = ("test@example.com",)
    with patch("auth.create_connection", return_value=mock_conn):
        result = register_user("test@example.com", "securepass")
        assert result is False
        mock_conn.commit.assert_not_called()

def test_authenticate_user_success(mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    hashed = bcrypt.hashpw(b"securepass", bcrypt.gensalt())
    mock_cursor.fetchone.return_value = (hashed,)
    with patch("auth.create_connection", return_value=mock_conn):
        result = authenticate_user("test@example.com", "securepass")
        assert result is True

def test_authenticate_user_wrong_password(mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    hashed = bcrypt.hashpw(b"correctpass", bcrypt.gensalt())
    mock_cursor.fetchone.return_value = (hashed,)
    with patch("auth.create_connection", return_value=mock_conn):
        result = authenticate_user("test@example.com", "wrongpass")
        assert result is False

def test_authenticate_user_not_found(mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_cursor.fetchone.return_value = None
    with patch("auth.create_connection", return_value=mock_conn):
        result = authenticate_user("nonexistent@example.com", "any")
        assert result is False

class DummyMessage:
    def __init__(self):
        self.text = ""
        self.replies = []
    async def reply_text(self, msg, **kwargs):
        self.replies.append(msg)

class DummyUpdate:
    def __init__(self, text):
        self.message = DummyMessage()
        self.message.text = text

class DummyContext:
    def __init__(self):
        self.user_data = {}
@pytest.mark.asyncio
async def test_random_fact_response():
    update = DummyUpdate("")
    context = DummyContext()
    await random_fact(update, context)
    assert update.message.replies
    assert "Факт" in update.message.replies[0]

@pytest.mark.asyncio
async def test_spending_advice_response():
    update = DummyUpdate("")
    context = DummyContext()
    await spending_advice(update, context)
    assert update.message.replies
    assert "Совет" in update.message.replies[0]

@pytest.mark.asyncio
async def test_roulette_win(monkeypatch):
    update = DummyUpdate("Красное")
    context = DummyContext()
    monkeypatch.setattr("roulette.random.choice", lambda x: "красное")
    with patch("roulette.return_to_main_menu", new_callable=AsyncMock):
        await handle_roulette_choice(update, context)
        assert "выиграли" in update.message.replies[0].lower()

@pytest.mark.asyncio
async def test_roulette_lose(monkeypatch):
    update = DummyUpdate("Красное")
    context = DummyContext()
    monkeypatch.setattr("roulette.random.choice", lambda x: "черное")
    with patch("roulette.return_to_main_menu", new_callable=AsyncMock):
        await handle_roulette_choice(update, context)
        assert "проиграли" in update.message.replies[0].lower()

@pytest.mark.asyncio
async def test_roulette_invalid_choice():
    update = DummyUpdate("Зеленое")
    context = DummyContext()
    await handle_roulette_choice(update, context)
    assert "выберите" in update.message.replies[0].lower()

@pytest.mark.asyncio
async def test_guess_too_low():
    update = DummyUpdate("20")
    context = DummyContext()
    context.user_data["number"] = 50
    await check_number(update, context)
    assert "маленькое" in update.message.replies[0].lower()

@pytest.mark.asyncio
async def test_guess_too_high():
    update = DummyUpdate("80")
    context = DummyContext()
    context.user_data["number"] = 30
    await check_number(update, context)
    assert "большое" in update.message.replies[0].lower()

@pytest.mark.asyncio
async def test_guess_correct():
    update = DummyUpdate("42")
    context = DummyContext()
    context.user_data["number"] = 42
    await check_number(update, context)
    assert "поздравляю" in update.message.replies[0].lower()
    assert "number" not in context.user_data
class MockResponse:
    def __init__(self, status, json_data):
        self.status = status
        self._json = json_data
    async def json(self):
        return self._json
    async def __aenter__(self):
        return self
    async def __aexit__(self, *args):
        pass

class MockSession:
    def __init__(self, response):
        self._response = response
    def get(self, *args, **kwargs):
        return self._response
    async def __aenter__(self):
        return self
    async def __aexit__(self, *args):
        pass

@pytest.mark.asyncio
async def test_weather_success(monkeypatch):
    update = DummyUpdate("")
    context = DummyContext()
    mock_response = MockResponse(200, {"main": {"temp": 10}, "weather": [{"description": "ясно"}]})
    monkeypatch.setattr("aiohttp.ClientSession", lambda: MockSession(mock_response))
    await weather(update, context)
    assert "температура" in update.message.replies[0].lower()

@pytest.mark.asyncio
async def test_weather_error(monkeypatch):
    update = DummyUpdate("")
    context = DummyContext()
    mock_response = MockResponse(404, {"message": "город не найден"})
    monkeypatch.setattr("aiohttp.ClientSession", lambda: MockSession(mock_response))
    await weather(update, context)
    assert "город не найден" in update.message.replies[0].lower()


import random
from random_fact import random_fact
from spending_advice import spending_advice
from roulette import handle_roulette_choice
from guess_number import check_number
from weather import weather

from unittest.mock import AsyncMock, patch

class DummyMessage:
    def __init__(self):
        self.text = ""
        self.replies = []
    async def reply_text(self, msg, **kwargs):
        self.replies.append(msg)

class DummyUpdate:
    def __init__(self, text):
        self.message = DummyMessage()
        self.message.text = text

class DummyContext:
    def __init__(self):
        self.user_data = {}

@pytest.mark.asyncio
async def test_random_fact_response():
    update = DummyUpdate("")
    context = DummyContext()
    await random_fact(update, context)
    assert update.message.replies
    assert "Факт" in update.message.replies[0]

@pytest.mark.asyncio
async def test_spending_advice_response():
    update = DummyUpdate("")
    context = DummyContext()
    await spending_advice(update, context)
    assert update.message.replies
    assert "Совет" in update.message.replies[0]

@pytest.mark.asyncio
async def test_roulette_win(monkeypatch):
    update = DummyUpdate("Красное")
    context = DummyContext()
    monkeypatch.setattr("roulette.random.choice", lambda x: "красное")
    with patch("roulette.return_to_main_menu", new_callable=AsyncMock):
        await handle_roulette_choice(update, context)
        assert "выиграли" in update.message.replies[0].lower()

@pytest.mark.asyncio
async def test_roulette_lose(monkeypatch):
    update = DummyUpdate("Красное")
    context = DummyContext()
    monkeypatch.setattr("roulette.random.choice", lambda x: "черное")
    with patch("roulette.return_to_main_menu", new_callable=AsyncMock):
        await handle_roulette_choice(update, context)
        assert "проиграли" in update.message.replies[0].lower()

@pytest.mark.asyncio
async def test_roulette_invalid_choice():
    update = DummyUpdate("Зеленое")
    context = DummyContext()
    await handle_roulette_choice(update, context)
    assert "выберите" in update.message.replies[0].lower()

@pytest.mark.asyncio
async def test_guess_too_low():
    update = DummyUpdate("20")
    context = DummyContext()
    context.user_data["number"] = 50
    await check_number(update, context)
    assert "маленькое" in update.message.replies[0].lower()

@pytest.mark.asyncio
async def test_guess_too_high():
    update = DummyUpdate("80")
    context = DummyContext()
    context.user_data["number"] = 30
    await check_number(update, context)
    assert "большое" in update.message.replies[0].lower()

@pytest.mark.asyncio
async def test_guess_correct():
    update = DummyUpdate("42")
    context = DummyContext()
    context.user_data["number"] = 42
    await check_number(update, context)
    assert "поздравляю" in update.message.replies[0].lower()
    assert "number" not in context.user_data

class MockResponse:
    def __init__(self, status, json_data):
        self.status = status
        self._json = json_data
    async def json(self):
        return self._json
    async def __aenter__(self):
        return self
    async def __aexit__(self, *args):
        pass

class MockSession:
    def __init__(self, response):
        self._response = response
    def get(self, *args, **kwargs):
        return self._response
    async def __aenter__(self):
        return self
    async def __aexit__(self, *args):
        pass

@pytest.mark.asyncio
async def test_weather_success(monkeypatch):
    update = DummyUpdate("")
    context = DummyContext()
    mock_response = MockResponse(200, {"main": {"temp": 10}, "weather": [{"description": "ясно"}]})
    monkeypatch.setattr("aiohttp.ClientSession", lambda: MockSession(mock_response))
    await weather(update, context)
    assert "температура" in update.message.replies[0].lower()

@pytest.mark.asyncio
async def test_weather_error(monkeypatch):
    update = DummyUpdate("")
    context = DummyContext()
    mock_response = MockResponse(404, {"message": "город не найден"})
    monkeypatch.setattr("aiohttp.ClientSession", lambda: MockSession(mock_response))
    await weather(update, context)
    assert "город не найден" in update.message.replies[0].lower()

def test_register_user_empty_email(mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    with patch("auth.create_connection", return_value=mock_conn):
        result = register_user("", "password")
        assert result is False

def test_register_user_short_password(mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    with patch("auth.create_connection", return_value=mock_conn):
        result = register_user("new@example.com", "123")
        assert isinstance(result, bool)

def test_authenticate_user_empty_password(mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_cursor.fetchone.return_value = (bcrypt.hashpw(b"", bcrypt.gensalt()),)
    with patch("auth.create_connection", return_value=mock_conn):
        result = authenticate_user("test@example.com", "")
        assert result is True

def test_guess_out_of_range_low():
    update = DummyUpdate("-10")
    context = DummyContext()
    context.user_data["number"] = 50
    import asyncio
    asyncio.run(check_number(update, context))
    assert "маленькое" in update.message.replies[0].lower()

def test_guess_out_of_range_high():
    update = DummyUpdate("1000")
    context = DummyContext()
    context.user_data["number"] = 42
    import asyncio
    asyncio.run(check_number(update, context))
    assert "большое" in update.message.replies[0].lower()