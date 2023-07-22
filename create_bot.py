from aiogram import Bot, Dispatcher
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage: MemoryStorage = MemoryStorage()

TOKEN: str = "6279675693:AAH50IJLtPUq37ryC5oGpmk1VYthLNg3AHM"
bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher(bot, storage=storage)
