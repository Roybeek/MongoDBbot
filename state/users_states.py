from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    started = State()
    get_name = State()
    get_surname = State()
    get_age = State()