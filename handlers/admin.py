from bot import *
from aiogram.dispatcher import FSMContext
from aiogram import types
from config import admin_ids
from markups import admin_kb, choice_rass_kb
from handlers import states
from aiogram.dispatcher.filters import Text

@dp.message_handler(commands=['admin'])
async def admin_cmd(message: types.Message):
    if message.from_user.id not in admin_ids:
        pass
    else:
        await message.answer('<i><b>Админ-меню</b></i>', reply_markup=admin_kb)

@dp.message_handler(lambda msg: msg.text == '📊 Статистика')
async def cmd_stats(message: types.Message):
    users = db.all_users()[0][0]
    await message.answer(f'<b>📊Статистика:</b>\n'
                         f'Пользователей: {users}')

@dp.message_handler(lambda msg: msg.text == '🔍 Поиск пользователя')
async def search_cmd(message: types.Message):
    await message.answer('Введите username пользователя:')
    await states.AdminStates.search_user.set()

@dp.callback_query_handler(Text(startswith='block_'))
async def block_user(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[1]
    db.block_user(user_id)
    await callback.message.edit_text('Юзер был забанен')

@dp.callback_query_handler(Text(startswith='bal_'))
async def set_balance(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.data.split('_')[1]
    await state.update_data(
        {
            'user_id': user_id
        }
    )
    await callback.message.edit_text('Введите сумму пополнения:\n\n'
                                     '(Если вы хотите снять деньги с баланса, припишите - к сумме)')
    await states.AdminStates.set_bal.set()

@dp.message_handler(lambda msg: msg.text == '👤 Добавить воркера')
async def add_worker(message: types.Message):
    await message.answer('Введите User-id пользователя:')
    await states.AdminStates.set_worker.set()

@dp.message_handler(lambda msg: msg.text == '👤 Удалить воркера')
async def add_worker(message: types.Message):
    await message.answer('Введите User-id пользователя:')
    await states.AdminStates.del_worker.set()

@dp.message_handler(lambda msg: msg.text == '📩 Рассылка')
async def rass_cmd(message: types.Message):
    await message.answer('Выберите тип рассылки:', reply_markup=choice_rass_kb)

@dp.callback_query_handler(lambda c: c.data == 'without_pic')
async def without_pic(callback: types.CallbackQuery):
    await callback.message.edit_text('Введите текст рассылки:')
    await states.AdminStates.without_pic.set()

@dp.callback_query_handler(lambda c: c.data == 'with_pic')
async def without_pic(callback: types.CallbackQuery):
    await callback.message.edit_text('Пришлите ссылку на картинку:\n\n'
                                     '(ПКМ по картинке -> Копировать URL картинки)')
    await states.AdminStates.with_pic_step1.set()

@dp.message_handler(lambda msg: msg.text == '🎟 Промокод')
async def add_promo(message: types.Message):
    await message.answer('Введите название промокода:')
    await states.AdminStates.set_name_promo.set()
