from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Познакомиться с ботом"),
        types.BotCommand("delete", "Удалить пользователя из Mongo"),
        types.BotCommand("show", "Показать всех пользователей"),
    ])

