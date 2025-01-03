from database import Database
from aiogram import Bot, Dispatcher
from config import bot_token
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=bot_token, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database('database.db')