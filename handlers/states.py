from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from bot import *
from payments import cp
from markups import *
from lolzapi import LolzApi
from crystalpay import InvoiceType
from config import lolz_token

lzt = LolzApi(lolz_token)

class UserStates(StatesGroup):
    up_balance = State()
    set_link = State()

class WorkerStates(StatesGroup):
    withdraw_bal = State()

class AdminStates(StatesGroup):
    search_user = State()
    set_bal = State()
    set_worker = State()
    del_worker = State()
    without_pic = State()
    with_pic_step1 = State()
    with_pic_step2 = State()
    set_name_promo = State()
    set_amount_promo = State()
    set_activations_promo = State()

@dp.message_handler(state=UserStates.up_balance)
async def up_balance(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
        invoice = cp.Invoice.create(amount, InvoiceType.topup, 15)
        await message.answer('<b>Для вас была зарезервирована ссылка для оплаты!</b>\n\n'
                             'Счет действителен 15 минут', reply_markup=payment(invoice['id'], invoice['url']))
    except:
        pass

    finally:
        await state.finish()

@dp.message_handler(state=UserStates.set_link)
async def set_link(message: types.Message, state: FSMContext):
    try:
        link = message.text
        a = link.split('=')
        b = a[1].split('&')[0]
        await state.update_data(
            {
                'link': link
            }
        )
        await message.answer(f'Ссылка на видео:\n'
                             f'<b>{link}</b>\n\n'
                             f'Желаете отправить видео на накрутку?', reply_markup=send_kb(b))
    except:
        await message.answer('Неправильная ссылка!')
    finally:
        await state.finish()

@dp.message_handler(state=WorkerStates.withdraw_bal)
async def withrdaw_balance(message: types.Message, state: FSMContext):
    try:
        data = db.worker_stats(message.from_user.id)
        amount = data[1]
        nickname = message.text
        a = lzt.send_money(amount, nickname)
        if not a.json().get('errors'):
            await message.answer('<b>✅ Средства были поставлены на вывод</b>')
        else:
            await message.answer('❌ <b>Произошла неизвестная ошибка.</b>\n'
                                 'Проверьте правильность написания вашего никнейма.\n\n'
                                 'Возможно, у администратора не хватает денег на балансе для совершения транзакций. Попробуйте позже.')

    finally:
        await state.finish()

@dp.message_handler(state=AdminStates.search_user)
async def search_state(message: types.Message, state: FSMContext):
    try:
        username = message.text
        data = db.search_user(username)
        await message.answer(f'<b>ℹ️ Информация о пользователе:</b>\n\n'
                             f'ID: {data[0]}\n'
                             f'Username: @{data[1]}\n'
                             f'Баланс: {data[2]} руб\n', reply_markup=features(data[0]))
    except TypeError:
        await message.answer('<b>❌ Такого ника в базе не найдено</b>')

    finally:
        await state.finish()

@dp.message_handler(state=AdminStates.set_bal)
async def set_balance(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
        data = await state.get_data()
        user_id = data.get('user_id')
        db.add_balance(user_id, amount)
        await message.answer('<b>✅ Действие было успешно совершено!</b>')

    except:
        await message.answer('<b>❌ Произошла неизвестная ошибка. </b>')

    finally:
        await state.finish()

@dp.message_handler(state=AdminStates.set_worker)
async def set_worker(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text)
        db.add_worker(user_id)
        await message.answer('<b>✅ Воркер был успешно добавлен</b>')
    except:
        await message.answer('<b>❌ Ошибка.</b>\n\n'
                             'Проверьте правильность написания USER-ID.')
    finally:
        await state.finish()

@dp.message_handler(state=AdminStates.del_worker)
async def set_worker(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text)
        db.del_worker(user_id)
        await message.answer('<b>✅ Воркер был успешно удален</b>')
    except:
        await message.answer('<b>❌ Ошибка.</b>\n\n'
                             'Проверьте правильность написания USER-ID.')
    finally:
        await state.finish()

@dp.message_handler(state=AdminStates.without_pic)
async def without_pic(message: types.Message, state: FSMContext):
    counter = 0
    count = db.all_users()
    try:
        users = db.get_users()
        msg = message.text
        for row in users:
            try:
                await bot.send_message(row[0], msg)
                counter += 1
                if int(row[1]) != 1:
                    db.set_active(row[0], 1)
            except:
                db.set_active(row[0], 0)
        await message.answer(f'<b>ℹ️ Рассылка завершена!</b>\n\n'
                             f'<b>Всего пользователей в базе: {count[0][0]}</b>\n'
                             f'<b>Получили сообщение: {counter} пользователей</b>')
    except:
        await message.answer('Произошла неизвестная ошибка')

    finally:
        await state.finish()

@dp.message_handler(state=AdminStates.with_pic_step1)
async def with_pic_step1(message: types.Message, state: FSMContext):
    photo = message.text
    await state.update_data(
        {
            'photo': photo
        }
    )
    await message.answer('Введите текст рассылки:')
    await AdminStates.with_pic_step2.set()

@dp.message_handler(state=AdminStates.with_pic_step2)
async def with_pic_step2(message: types.Message, state: FSMContext):
    counter = 0
    data = await state.get_data()
    photo = data.get('photo')
    count = db.all_users()
    msg = message.text
    users = db.get_users()
    try:
        for row in users:
            try:
                await bot.send_photo(chat_id=row[0], photo=photo, caption=msg)
                counter += 1
                if int(row[1]) != 1:
                    db.set_active(row[0], 1)
            except:
                db.set_active(row[0], 0)
    finally:
        await state.finish()

    await message.answer(f'<b>ℹ️ Рассылка завершена!</b>\n\n'
                            f'<b>Всего пользователей в базе: {count[0][0]}</b>\n'
                            f'<b>Получили сообщение: {counter} пользователей</b>')

@dp.message_handler(state=AdminStates.set_name_promo)
async def set_amount(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'name': name
        }
    )
    await message.answer('Введи сумму промокода:')
    await AdminStates.set_amount_promo.set()

@dp.message_handler(state=AdminStates.set_amount_promo)
async def set_activ(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
        await state.update_data(
            {
                'amount': amount
            }
        )
        await message.answer('Введите кол-во активаций:')
        await AdminStates.set_activations_promo.set()
    except:
        await message.answer('Вы ввели не число!')
        await state.finish()

@dp.message_handler(state=AdminStates.set_activations_promo)
async def add_promo(message: types.Message, state: FSMContext):
    try:
        activations = int(message.text)
        data = await state.get_data()
        name, amount = data.get('name'), data.get('amount')
        db.add_promo(name, amount, activations)
        await message.answer('Промокод создан!')
    except:
        await message.answer('Вы ввели не число!')

    finally:
        await state.finish()



