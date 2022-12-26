from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    first_name = State()
    last_name = State()
    email = State()
    phone_number = State()
    birth_day = State()
