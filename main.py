from bot import dp
from handlers import start, user, worker, admin
from aiogram import executor

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
