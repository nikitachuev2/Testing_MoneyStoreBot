from behave import given, when, then
from auth import register_user, authenticate_user
from random_fact import random_fact
from spending_advice import spending_advice
from roulette import handle_roulette_choice
from guess_number import check_number
from weather import weather
import asyncio
import sqlite3
class DummyMessage:
    def __init__(self):
        self.text = ""
        self.replies = []
    async def reply_text(self, msg, **kwargs):
        self.replies.append(msg)

class DummyUpdate:
    def __init__(self, text=""):
        self.message = DummyMessage()
        self.message.text = text

class DummyContext:
    def __init__(self):
        self.user_data = {}

@given('Пользователь с почтой "{email}" уже существует')
def step_user_already_exists(context, email):
    register_user(email, "secure")

@given('Я ввел почту "{email}"')
def step_given_email(context, email):
    context.email = email

@given('Я ввел пароль "{password}"')
def step_given_password(context, password):
    context.password = password

@when("Я пытаюсь зарегистрироваться")
def step_when_register(context):
    context.result = register_user(context.email, context.password)

@then("Регистрация должна быть успешной")
def step_then_register_success(context):
    assert context.result is True

@then('Должна быть ошибка "Пользователь уже существует"')
def step_then_registration_exists(context):
    assert context.result is False

@when("Я пытаюсь войти")
def step_when_login(context):
    context.result = authenticate_user(context.email, context.password)

@then("Авторизация должна быть успешной")
def step_then_auth_success(context):
    assert context.result is True

@then('Должна быть ошибка "Неверный email или пароль"')
def step_then_auth_failed(context):
    assert context.result is False

@when("Я запрашиваю случайный факт")
def step_when_fact(context):
    context.update = DummyUpdate()
    context.ctx = DummyContext()
    import asyncio
    asyncio.run(random_fact(context.update, context.ctx))

@then('Я должен получить ответ в чате от бота, содержащий "Факт"')
def step_then_fact(context):
    assert any("Факт" in r for r in context.update.message.replies)

@when("Я запрашиваю погоду")
def step_weather_request(context):
    context.update = DummyUpdate()
    context.ctx = DummyContext()
    asyncio.run(weather(context.update, context.ctx))

@then("Я должен получить температуру и описание")
def step_weather_response(context):
    assert context.update.message.replies
    assert "температура" in context.update.message.replies[0]

@given("Я начинаю игру угадай число")
def step_start_guess_game(context):
    context.ctx = DummyContext()
    context.ctx.user_data["number"] = 42

@when("Я угадываю число")
def step_correct_guess(context):
    context.update = DummyUpdate("42")
    asyncio.run(check_number(context.update, context.ctx))

@then("Я должен получить сообщение о победе с поздравлением")
def step_check_win(context):
    assert any("поздравляю" in r.lower() for r in context.update.message.replies)

@when("Я ввожу число меньше загаданного")
def step_low_guess(context):
    context.update = DummyUpdate("20")
    asyncio.run(check_number(context.update, context.ctx))

@then('Я должен получить подсказку "меньше"')
def step_hint_low(context):
    assert any("маленькое" in r.lower() for r in context.update.message.replies)

@given('Я выбираю "красное"')
def step_choose_red(context):
    context.update = DummyUpdate("Красное")
    context.ctx = DummyContext()

@when('Выпадает "красное"')
def step_force_red(context):
    from roulette import random
    random.choice = lambda x: "красное"

@then("Я выиграл")
def step_win_roulette(context):
    asyncio.run(handle_roulette_choice(context.update, context.ctx))
    assert any("выиграли" in r.lower() for r in context.update.message.replies)

@when("Я запрашиваю совет")
def step_advice(context):
    context.update = DummyUpdate()
    context.ctx = DummyContext()
    asyncio.run(spending_advice(context.update, context.ctx))

@then('Я должен получить "Совет" от бота')
def step_advice_text(context):
    assert any("Совет" in r for r in context.update.message.replies)



@given('Я удаляю пользователя "{email}"')
def step_delete_user(context, email):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password BLOB NOT NULL)"
    )
    cur.execute("DELETE FROM users WHERE email = ?", (email,))
    conn.commit()
    conn.close()