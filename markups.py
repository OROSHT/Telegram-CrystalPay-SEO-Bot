from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

profile_btn = KeyboardButton('👤 Профиль')
seo_btn = KeyboardButton('🔺 Накрутка SEO')

main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    profile_btn, seo_btn
)

"""____________________________"""

up_bal_btn = InlineKeyboardButton('Пополнить счет', callback_data='up_bal')
profile_inline = InlineKeyboardMarkup().add(
    up_bal_btn
)
"""_____________________________"""
crystalpay_btn = InlineKeyboardButton('Crypto | LOLZ', callback_data='crypto')
back_btn = InlineKeyboardButton('◀️ Назад', callback_data='back')
payments_kb = InlineKeyboardMarkup(row_width=1).add(
    crystalpay_btn, back_btn
)

"""______________________________"""

def payment(id, url):
    kb1 = InlineKeyboardMarkup(row_width=1)
    link_payment = InlineKeyboardButton('Оплатить', url=url)
    verify_payment = InlineKeyboardButton('Проверить оплату', callback_data=f'verify_{id}')
    kb1.add(
        link_payment, verify_payment
    )
    return kb1

"""_______________________________"""

def send_kb(auth_id):
    accept_btn = InlineKeyboardButton('✅ Отправить', callback_data=f'accept_{auth_id}')
    decline_btn = InlineKeyboardButton('❌ Отклонить', callback_data='decline')
    kb1 = InlineKeyboardMarkup(row_width=2).add(
        accept_btn, decline_btn
    )
    return kb1

"""________________________________"""

def orders_kb(data):
    orders_keyboard = InlineKeyboardMarkup(row_width=1)
    for i in data:
        orders_keyboard.insert(InlineKeyboardButton(f'ID: {i[0]} | @{i[2]}', callback_data=f'order_{i[0]}'))
    return orders_keyboard

worker_profile_btn = KeyboardButton('Профиль')
worker_orders_btn = KeyboardButton('Мои заказы')
get_order_btn = KeyboardButton('Взять заказ')
worker_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    worker_profile_btn, worker_orders_btn, get_order_btn
)

withdraw_btn = InlineKeyboardButton('Вывести средства', callback_data='withdraw')
keyboard_withdr = InlineKeyboardMarkup().add(
    withdraw_btn
)

"""___________________________________"""

def order_worker(user_id, id_):
    kb1 = InlineKeyboardMarkup(row_width=2)
    accept_btn = InlineKeyboardButton('Принять', callback_data=f'accwork_{user_id}_{id_}')
    back_btn = InlineKeyboardButton('В меню', callback_data='backwork')
    kb1.add(
        accept_btn, back_btn
    )
    return kb1

"""_____________________________________"""

def worker_orders(data):
    kb1 = InlineKeyboardMarkup(row_width=1)
    for i in data:
        kb1.insert(InlineKeyboardButton(f'ID: {i[2]} | @{i[1]}', callback_data=f'worker_{i[2]}'))
    return kb1

"""______________________________________"""

def seo(user_id, id_):
    seo_finished_btn = InlineKeyboardButton('✅ SEO встало', callback_data=f'seodone_{user_id}_{id_}')
    seo_not_finished = InlineKeyboardButton('❌ SEO не встало', callback_data=f'seonotdone_{user_id}_{id_}')
    seo_kb = InlineKeyboardMarkup(row_width=2).add(
        seo_finished_btn, seo_not_finished
    )
    return seo_kb

"""_________________________________________"""

search_user_btn = KeyboardButton('🔍 Поиск пользователя')
stats_btn = KeyboardButton('📊 Статистика')
add_worker = KeyboardButton('👤 Добавить воркера')
del_worker = KeyboardButton('👤 Удалить воркера')
rass_btn = KeyboardButton('📩 Рассылка')
promocode_btn = KeyboardButton('🎟 Промокод')
admin_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
    search_user_btn, stats_btn, add_worker, del_worker, rass_btn, promocode_btn
)

def features(user_id):
    ban_btn = InlineKeyboardButton('❌ Заблокировать', callback_data=f'block_{user_id}')
    send_message_btn = InlineKeyboardButton('💬 Отправить сообщение', callback_data=f'send_{user_id}')
    set_balance_btn = InlineKeyboardButton('💰 Выдать/забрать баланс', callback_data=f'bal_{user_id}')
    kb1 = InlineKeyboardMarkup(row_width=2).add(
        ban_btn, send_message_btn, set_balance_btn
    )
    return kb1

without_pic_btn = InlineKeyboardButton('❌ Без картинки', callback_data='without_pic')
with_pic_btn = InlineKeyboardButton('🖼 С картинкой', callback_data='with_pic')
choice_rass_kb = InlineKeyboardMarkup(row_width=2).add(
    with_pic_btn, without_pic_btn
)

