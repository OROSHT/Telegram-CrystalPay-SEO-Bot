from bot import *
from aiogram.dispatcher.filters import Text
from aiogram import types
from markups import *
from handlers import states
from config import price, worker_percent


@dp.message_handler(commands=['worker'])
async def cmd_worker(message: types.Message):
    if not db.worker_exists(message.from_user.id):
        pass
    else:
        await message.answer('<i><b>Меню воркера</b></i>', reply_markup=worker_kb)

@dp.message_handler(lambda msg: msg.text == 'Профиль')
async def cmd_worker_profile(message: types.Message):
    if not db.worker_exists(message.from_user.id):
        pass
    else:
        data = db.worker_stats(message.from_user.id)
        await message.answer(f'📱 Профиль:\n'
                             f'💰 Баланс воркера: {data[1]} руб', reply_markup=keyboard_withdr)

@dp.message_handler(lambda msg: msg.text == 'Мои заказы')
async def my_orders(message: types.Message):
    if not db.worker_exists(message.from_user.id):
        pass
    else:
        data = db.worker_orders(message.from_user.id)
        await message.answer('Ваши заказы:', reply_markup=worker_orders(data))

@dp.message_handler(lambda msg: msg.text == 'Взять заказ')
async def get_order(message: types.Message):
    if not db.worker_exists(message.from_user.id):
        pass
    else:
        data = db.orders()
        await message.answer('Непринятые заказы:',
                             reply_markup=orders_kb(data))

@dp.callback_query_handler(Text(startswith='order_'))
async def order_info(callback: types.CallbackQuery):
    id_ = callback.data.split('_')[1]
    data = db.get_order_info(id_)
    await callback.message.edit_text(f'<b>Заявка от @{data[2]}</b>\n\n'
                                     f'Ссылка на видео: <b>{data[3]}</b>',
                                     reply_markup=order_worker(data[1], data[0]))

@dp.callback_query_handler(Text(startswith='accwork_'))
async def cmd_accept(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[1]
    id_ = callback.data.split('_')[2]
    data = db.get_order_info(id_)
    db.set_order_to_worker(callback.from_user.id, user_id, id_, data[3])
    db.delete_order(id_)
    await callback.message.edit_text('<b>Заказ был принят!</b>')

@dp.callback_query_handler(lambda c: c.data == 'backwork')
async def back_cmd(callback: types.CallbackQuery):
    data = db.orders()
    await callback.message.edit_text('Непринятые заказы:',
                         reply_markup=orders_kb(data))


@dp.callback_query_handler(Text(startswith='worker_'))
async def order_info(callback: types.CallbackQuery):
    id_ = callback.data.split('_')[1]
    data = db.get_accepted_order(id_)
    await callback.message.edit_text(f'📄 Заказ #{id_}\n\n'
                                     f'👤 Заказчик: {data[1]}\n'
                                     f'🔗 Ссылка на видео: {data[3]}', reply_markup=seo(data[1], id_))

@dp.callback_query_handler(Text(startswith='seodone_'))
async def seo_done_cmd(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[1]
    id_ = callback.data.split('_')[2]
    data = db.get_accepted_order(id_)
    db.add_worker_balance(callback.from_user.id, price/100*worker_percent)
    await callback.message.edit_text('✅ Сообщение отправлено заказчику')
    await bot.send_message(user_id, f'<b>✅ Ваша заявка на SEO была выполнена!</b>\n'
                                    f'<b>🔗 Ссылка на видео: {data[3]}</b>')
    db.delete_accepted_order(id_)

@dp.callback_query_handler(Text(startswith='seonotdone_'))
async def seo_done_cmd(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[1]
    id_ = callback.data.split('_')[2]
    data = db.get_accepted_order(id_)
    await callback.message.edit_text('✅ Сообщение отправлено заказчику')
    await bot.send_message(user_id, f'<b>❌ Ваша заявка на SEO была отклонена!</b>\n'
                                    f'<b>🔗 Ссылка на видео: {data[3]}</b>\n'
                                    f'<b>Деньги были возвращены на ваш баланс</b>')
    db.delete_accepted_order(id_)
    db.add_balance(user_id, price)

@dp.callback_query_handler(lambda c: c.data == 'withdraw')
async def withdraw_btn(callback: types.CallbackQuery):
    await callback.message.edit_text('Введите ник своего LOLZTEAM-аккаунта:\n\n'
                                     '<b>Если вы укажите неправильный ник, средства могут быть потеряны!</b>')
    await states.WorkerStates.withdraw_bal.set()