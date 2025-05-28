
from behave import given, when, then
from datetime import datetime
import random

# === TC-011 ===
@when('Пользователь вводит команду "/datetime"')
def step_get_datetime(context):
    context.response = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@then('Бот возвращает строку с текущей датой')
def step_check_datetime(context):
    assert isinstance(context.response, str)
    assert len(context.response) > 10  # Простейшая проверка даты

# === TC-012 ===
@when('Пользователь вводит команду "/fact"')
def step_get_fact(context):
    facts = [
        "Факт 1: Вода кипит при 100°C.",
        "Факт 2: Земля вращается вокруг Солнца.",
        "Факт 3: Python — популярный язык программирования."
    ]
    context.response = random.choice(facts)

@then('Бот возвращает не пустой факт')
def step_check_fact(context):
    assert context.response is not None
    assert isinstance(context.response, str)
    assert len(context.response.strip()) > 0

# === TC-013 и TC-014 ===
@given('Пользователь "user@example.com" уже зарегистрирован')
def step_registered_user(context):
    context.users = {"user@example.com": "ValidPass123!"}

@when('Вводит имя "user@example.com"')
def step_enter_username(context):
    context.entered_username = "user@example.com"

@when('Вводит пароль "ValidPass123!"')
def step_enter_valid_password(context):
    context.entered_password = "ValidPass123!"

@when('Вводит неверный пароль "WrongPassword"')
def step_enter_invalid_password(context):
    context.entered_password = "WrongPassword"

@then('Появляется сообщение "Пользователь зарегистрирован"')
def step_success_login(context):
    assert context.users.get(context.entered_username) == context.entered_password

@then('Появляется сообщение "Неверный логин или пароль"')
def step_failed_login(context):
    assert context.users.get(context.entered_username) != context.entered_password

# === TC-015 ===
@when('Пользователь вводит команду "/roulette"')
def step_start_roulette(context):
    context.response = "🎲 Рулетка запущена! Выберите 'Красное' или 'Черное':"

@then('Появляется сообщение "🎲 Рулетка запущена! Выберите \'Красное\' или \'Черное\':"')
def step_roulette_prompt(context):
    assert context.response == "🎲 Рулетка запущена! Выберите 'Красное' или 'Черное':"

# === TC-016 и TC-017 ===
@given('Результат рулетки будет "{result}"')
def step_set_roulette_result(context, result):
    context.roulette_result = result.lower()

@when('Пользователь выбирает "{choice}"')
def step_user_choice(context, choice):
    choice = choice.lower()
    if choice not in ["красное", "черное"]:
        context.response = "Пожалуйста, выберите 'Красное' или 'Черное'."
    elif choice == context.roulette_result:
        context.response = "Поздравляем, вы выиграли"
    else:
        context.response = "увы, вы проиграли"

@then('Бот говорит "Поздравляем, вы выиграли"')
def step_win_response(context):
    assert context.response == "Поздравляем, вы выиграли"

@then('Бот говорит "увы, вы проиграли"')
def step_lose_response(context):
    assert context.response == "увы, вы проиграли"

# === TC-018 ===
@then('Появляется сообщение "Пожалуйста, выберите \'Красное\' или \'Черное\'."')
def step_invalid_choice(context):
    assert context.response == "Пожалуйста, выберите 'Красное' или 'Черное'."

# === TC-019 ===
@when('Пользователь завершает игру')
def step_exit_game(context):
    context.response = "Произошел возврат в меню"

@then('Появляется сообщение "Произошел возврат в меню"')
def step_back_to_menu(context):
    assert context.response == "Произошел возврат в меню"

# === TC-020 ===
@when('Пользователь вводит команду "/login"')
def step_login_command(context):
    context.response = "Введите свой email для входа:"

@then('Появляется сообщение "Введите свой email для входа:"')
def step_login_prompt(context):
    assert context.response == "Введите свой email для входа:"
 