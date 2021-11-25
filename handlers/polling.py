from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.types import CallbackQuery

from loader import dp
from state.users_states import UserStates
from classes import User


@dp.message_handler(CommandStart(), state="*")  # Ввели команду старт
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer("Привет!")
    tg_user = User(message.from_user.id)

    if tg_user.check_db_user():
        await message.answer(f"О! А я с Вами знаком!\n"
                             f"Вы {tg_user.surname} {tg_user.name}\n"
                             f"Вам {tg_user.age}")
    else:
        await message.answer("Я с Вами не знаком. Давайте знакомиться?\n"
                             "Напишите Ваше имя?")
        await UserStates.get_name.set()


@dp.message_handler(state=UserStates.get_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите фамилию?")
    await UserStates.get_surname.set()


@dp.message_handler(state=UserStates.get_surname)
async def get_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Введите Ваш возраст?")
    await UserStates.get_age.set()


@dp.message_handler(state=UserStates.get_age)
async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Приятно познакомиться, я постараюсь Вас запомнить!")
    user_info = await state.get_data()
    tg_user = User(message.from_user.id)
    tg_user.update_user_info(user_info.get('name'), user_info.get('surname'), user_info.get('age'))
    msg = tg_user.get_user_info()
    await message.answer(msg)
    await state.finish()


@dp.message_handler(Command("delete"), state='*')
async def get_delete(message: types.Message, state: FSMContext):

    tg_user = User(message.from_user.id)
    if tg_user.check_db_user():
        await message.answer("Чтож, придется прощаться...")
        tg_user.remove_db_user()
    else:
        await message.answer("Такого пользователя нет в моей базе, нажмите /start чтобы познакомиться")


@dp.message_handler(Command("show"), state='*')
async def show_all(message: types.Message, state: FSMContext):

    tg_user = User(message.from_user.id)
    await message.answer(tg_user.get_all_users())
