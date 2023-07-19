from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

TOKEN = "6279675693:AAH50IJLtPUq37ryC5oGpmk1VYthLNg3AHM"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
