import sqlite3
from aiogram.dispatcher.filters import Text
from aiogram import types
from bot import *
from config import price
from markups import *
from payments import cp
from handlers import states

@dp.message_handler(lambda msg: msg.text == '👤 Профиль')
async def cmd_profile(message: types.Message):
    data = db.stats(message.from_user.id)
    if data[5] == 1:
        await message.answer('Вы заблокированы')
    else:
        await message.answer(f'📱 Ваш профиль:\n'
                            f'➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                            f'🔑 ID: {message.from_user.id}\n'
                            f'👤 Логин: @{message.from_user.username}\n\n'
                            f'➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                            f'💳 Баланс: {data[2]} руб\n'
                            f'💵 Всего заказов на сумму: {data[3]} руб\n'
                            f'🎁 Всего заказов: {data[4]} шт.', reply_markup=profile_inline)

@dp.message_handler(lambda msg: msg.text == '🔺 Накрутка SEO')
async def seo_up(message: types.Message):
    data = db.stats(message.from_user.id)
    if data[5] == 1:
        await message.answer('Вы заблокированы')
    else:
        await message.answer(f'Стоимость накрутки - {price} рублей\n'
                             'Предоставьте ссылку на видео, на которое нужно накрутить SEO:\n\n'
                            '❗️ <b>Важно - видео должно быть залито не более часа назад и иметь SEO от 50</b>')
        await states.UserStates.set_link.set()

@dp.callback_query_handler(lambda c: c.data == 'up_bal')
async def up_balance(callback: types.CallbackQuery):
    data = db.stats(callback.from_user.id)
    if data[5] == 1:
        await callback.message.answer('Вы заблокированы')
    else:
        await callback.message.edit_text('Выберите платежный метод:', reply_markup=payments_kb)

@dp.callback_query_handler(lambda c: c.data == 'back')
async def back_cmd(callback: types.CallbackQuery):
    data = db.stats(callback.from_user.id)
    if data[5] == 1:
        await callback.message.answer('Вы заблокированы')
    else:
        data = db.stats(callback.from_user.id)
        await callback.message.edit_text(f'📱 Ваш профиль:\n'
                                     f'➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                     f'🔑 ID: {callback.from_user.id}\n'
                                     f'👤 Логин: @{callback.from_user.username}\n\n'
                                     f'➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                     f'💳 Баланс: {data[2]} руб\n'
                                     f'💵 Всего заказов на сумму: {data[3]} руб\n'
                                     f'🎁 Всего заказов: {data[4]} шт.', reply_markup=profile_inline)

@dp.callback_query_handler(lambda c: c.data == 'crypto')
async def invoice(callback: types.CallbackQuery):
    data = db.stats(callback.from_user.id)
    if data[5] == 1:
        await callback.message.answer('Вы заблокированы')
    else:
        await callback.message.edit_text('Введите сумму пополнения:')
        await states.UserStates.up_balance.set()

@dp.callback_query_handler(Text(startswith='verify'))
async def verify_invoice(callback: types.CallbackQuery):
    invoice_id = callback.data.split('_', maxsplit=1)[1]
    invoice_info = cp.Invoice.getinfo(invoice_id)
    if invoice_info['state'] == 'payed':
        db.add_balance(callback.from_user.id, invoice_info['amount'])
        await callback.message.edit_text('<b>✅ Счет был успешно пополнен!</b>')
    else:
        await callback.answer('❌ Счет не оплачен')

@dp.callback_query_handler(Text(startswith='accept_'))
async def accept_cmd(callback: types.CallbackQuery):
    data = db.stats(callback.from_user.id)
    if data[5] == 1:
        await callback.message.answer('Вы заблокированы')
    else:
        authenticator = callback.data.split('_', maxsplit=1)[1]
        data = db.stats(callback.from_user.id)
        if data[2] < price:
            await callback.answer('Недостаточно средств')
        else:
            try:
                db.minus_balance(callback.from_user.id, price)
                db.add_order(callback.from_user.id, callback.from_user.username, f'https://www.youtube.com/watch?v={authenticator}')
                db.set_all_money(callback.from_user.id, price)
                db.set_all_orders(callback.from_user.id)
                for i in db.workers():
                    await bot.send_message(i[0], '<b>🔔 Пришло новое видео на накрутку!</b>\nСкорее иди крутить!')
                await callback.message.edit_text('<b>✅ Видео отправлено на накрутку</b>')
            except sqlite3.IntegrityError:
                db.add_balance(callback.from_user.id, price)
                await callback.message.edit_text('❌ <b>Произошла ошибка</b>\n'
                                             'Вероятно, вы уже отправили это видео на накрутку. Ожидайте.')

@dp.callback_query_handler(lambda c: c.data == 'decline')
async def decline_cmd(callback: types.CallbackQuery):
    data = db.stats(callback.from_user.id)
    if data[5] == 1:
        await callback.message.answer('Вы заблокированы')
    else:
        data = db.stats(callback.from_user.id)
        await callback.message.edit_text('<b>❌ Действие отменено</b>')
        await callback.message.answer(f'📱 Ваш профиль:\n'
                                     f'➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                     f'🔑 ID: {callback.from_user.id}\n'
                                     f'👤 Логин: @{callback.from_user.username}\n\n'
                                     f'➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                     f'💳 Баланс: {data[2]} руб\n'
                                     f'💵 Всего заказов на сумму: {data[3]} руб\n'
                                     f'🎁 Всего заказов: {data[4]} шт.', reply_markup=profile_inline)

@dp.message_handler(commands=['promo'])
async def promo(message: types.Message):
    try:
        promo = message.text.split(' ')[1]
        data = db.get_promo(promo)
        promo_db = data[0]
        if promo == promo_db:
            if data[2] != 0:
                db.add_balance(message.from_user.id, data[1])
                db.minus_activ(promo_db)
                await message.answer('<b>Промокод успешно активирован!</b>')
            else:
                db.delete_promo(promo)
    except IndexError:
        await message.answer('Вы не ввели промокод. Используйте /promo *промокод*')
    except TypeError:
        await message.answer('Промокод не найден!')





