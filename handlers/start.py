from aiogram import types
from bot import *
from config import admin_ids
from markups import main_kb

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.username)
        for i in admin_ids:
            await bot.send_message(i, f'<b>Зашел новый пользователь: @{message.from_user.username}</b>')
    await message.answer('<b><i>Главное меню</i></b>', reply_markup=main_kb)