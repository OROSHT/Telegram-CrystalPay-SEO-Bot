from bot import *
from config import auth_login, secret_1, secret_2
from aiogram import types
from crystalpay import *

cp = CrystalPAY(auth_login, secret_1, secret_2)