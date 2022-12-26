import asyncio
import datetime
import logging
import os

import registration
import requests
import validators
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from quick_commands import create_user
from selenium import webdriver

logging.basicConfig(level=logging.INFO)

load_dotenv()

TOKEN_BOT = os.getenv('BOT_API')

bot = Bot(TOKEN_BOT)

dp = Dispatcher(bot, storage=MemoryStorage())

url = str(os.getenv('URL'))


@dp.message_handler()
async def begin(message: types.Message):
    """
    Отправка скриншота.
    """
    request = requests.get(url=url)
    soup = BeautifulSoup(request.content, 'html.parser')
    print(soup)
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    driver = webdriver.Chrome(chrome_options=option)
    driver.get(url)

    driver.execute_script('window.scrollTo(0,300')
    file_name = driver.save_screenshot(
        f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M"),message.from_user.id}.jpg'
    )
    file_path = os.path.join(r'C:\Dev\tg_bot_testovoe\images', file_name)
    with open(file_path, 'w') as file:
        file.write()
    driver.close()

    photo = open(file_name, 'rb')
    await bot.send_photo(
        message.chat.id,
        photo=photo,
        caption='Можешь перейти на сайт',
        parse_mode='HTML'
    )


dp.message_handler()
async def check_site_activate(url, time_wait):
    """
    Проверка наличия пользователя в бд.
    """
    while True:
        try:
            response = requests.get(url=url)
            if response.status_code == 200:
                print('Сайт работает, все хорошо')
        except Exception:
            print('К сожалению в настоящий сайт не досупен')
        finally:
            await asyncio.sleep(time_wait)


@dp.message_handler(commands=['start'])
async def crete_user(message: types.Message):
    """
    Создание записи пользователя в бд.
    """
    user = message.from_user.id
    if user:
        await message.answer(
            f'Здравствуйте, {message.from_user.username} вы зарегистрированы'
        )
        dp.stop_polling()

    else:
        await message.answer('Для регистрации введите свое имя:')
        await registration.Registration.first_name.set()


@dp.message_handler(state=registration.Registration.first_name)
async def get_first_name(message: types.Message, state: FSMContext):
    """
    Имя.
    """
    first_name = message.text

    if validators.validate_name(first_name):
        await state.update_data(first_name=first_name)
        await message.answer(
            f'{first_name}, теперь будь любезен пришли мне свою фамилию'
        )
        await registration.Registration.last_name.set()
    else:
        await message.answer(
            text=(
                'Пожалуйста, потвторите попытку, имя не содерджать цифры'
                'и иные символы, кроме букв'
            ))


@dp.message_handler(state=registration.Registration.last_name)
async def get_last_name(message: types.Message, state: FSMContext):
    """
    Фамилия.
    """
    last_name = message.text

    if validators.validate_name(last_name):
        await state.update_data(last_name=last_name)
        await message.answer('Жду вашу почту )')
        await registration.Registration.email.set()
    else:
        await message.answer(
            text=(
                'Пожалуйста, потвторите попытку, имя не содерджать цифры'
                'и иные символы, кроме букв'
            ))


@dp.message_handler(state=registration.Registration.email)
async def get_email_user(message: types.Message, state: FSMContext):
    """
    Почта.
    """
    email = message.text

    if validators.validate_email(email):
        await state.update_data(email=email)
        await message.answer(
            'Осталось еще немного, введите ваш номер телефона:'
        )
        await registration.Registration.phone_number.set()
    else:
        await message.answer(text='Не корректный email-адрес')


@dp.message_handler(state=registration.Registration.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    """
    Телефон.
    """
    phone_number = message.text

    if validators.validate_phone_number(phone_number):
        await state.update_data(phone_number=phone_number)
        await message.answer('Последний шаг, укажите вашу дату рождения:')
        await registration.Registration.birth_day.set()
    else:
        await message.answer(text='Введите корректный номер телефона')


@dp.message_handler(state=registration.Registration.birth_day)
async def get_birth_day(message: types.Message, state: FSMContext):
    """
    День рождения.
    """
    birth_day = message.text
    if validators.validate_birth_day(birth_day):
        await state.update_data(birth_day=birth_day)
        data = await state.get_data()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        birth_day = data.get('birth_day')
        status = 'active'
        await create_user(
            message.from_user.id,
            first_name, last_name,
            email, phone_number, birth_day, status
        )
        await message.answer(
            f'Регистрация прошла успешна\n'
            f'Имя: {first_name}\n'
            f'Фамилия: {last_name}\n'
            f'Email: {email}\n'
            f'Номер телефона: {phone_number}\n'
            f'Дата рождения: {birth_day}'
        )
        await check_site_activate(message)
        await state.finish()

    else:
        await message.answer(
            text='Дата рождения введена не корректно (день-месяц-год)'
        )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(check_site_activate(url, 600))
    executor.start_polling(dp, skip_updates=True)
