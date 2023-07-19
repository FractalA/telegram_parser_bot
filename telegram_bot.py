from aiogram.utils import executor
from handlers import client, admin, other
from create_bot import dp


client.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


