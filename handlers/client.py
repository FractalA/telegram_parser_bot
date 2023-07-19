from aiogram import types, Dispatcher
from keyboards import kb_client
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import sqlite3
from script import ad_search
from datetime import datetime, timedelta


async def start(message: types.Message):
    await message.answer("Бот для мониторинга объявлений", reply_markup=kb_client)


async def show_all(message: types.Message):
    base = sqlite3.connect("cars.db")
    cur = base.cursor()
    for elem in cur.execute("SELECT * FROM data ORDER BY data DESC").fetchall():
        await message.answer(f"{elem[2]}\n{elem[1]}\n{elem[0]}")
    base.close()


async def show_new(message: types.Message):
    await message.answer("Функция 'Вывести новые', выводит объявления\n"
                         "Которые были добавлены в интервале между двумя последними обновлениями базы данных")
    base = sqlite3.connect("cars.db")
    cur = base.cursor()
    user_id = message.from_user.id
    query = "SELECT time FROM users WHERE user_id = ?"
    result = cur.execute(query, (user_id,)).fetchone()
    last_viewed_time = result[0] if result else None
    if last_viewed_time:
        query = "SELECT * FROM data WHERE data >= ?"
        new_ads = cur.execute(query, (last_viewed_time,)).fetchall()

        if new_ads:
            await message.answer("Новые объявления:")
            for elem in new_ads:
                await message.answer(f"{elem[2]}\n{elem[1]}\n{elem[0]}")
        else:
            await message.answer("Нет новых объявлений")
    base.close()

class FSMAdmin(StatesGroup):
    number_ads = State()
    url = State()


async def show(message: types.Message):
    await FSMAdmin.number_ads.set()
    await message.reply("Введите количество объявлений")


async def get_number(message: types.Message, state: FSMContext):
    base = sqlite3.connect("cars.db")
    cur = base.cursor()

    async with state.proxy() as data:
        data["number_ads"] = int(message.text)
        for elem in cur.execute(f"SELECT * FROM data ORDER BY data DESC LIMIT {data['number_ads']}").fetchall():
            await message.answer(f"{elem[2]}\n{elem[1]}\n{elem[0]}")
        await state.finish()
    base.close()


async def cancel(message: types.Message, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Действие отменено")
    

async def update(message: types.Message):
    base = sqlite3.connect("cars.db")
    cur = base.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(user_id PRIMARY KEY, time)")
    query = """
    INSERT OR REPLACE INTO users (user_id, time)
    VALUES (?, ?)
    """
    time_now = datetime.now()
    time_current = time_now - timedelta(minutes=2)
    time_current_str = time_current.strftime("%Y-%m-%d %H:%M:%S")
    await message.answer("Обновление базы данных...\nОжидайте")
    await ad_search.show_cars()
    await message.answer("База данных обновлена")
    await message.answer(f"Время обновления базы данных - {time_now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    cur.execute(query, (message.from_user.id, time_current_str))
    base.commit()
    base.close()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(show_all, lambda message: "Вывести все объявления" in message.text)
    dp.register_message_handler(show_new, lambda message: "Вывести новые" in message.text)
    dp.register_message_handler(show, lambda message: "Выбрать кол-во объявлений" in message.text, state=None)
    dp.register_message_handler(get_number, state=FSMAdmin.number_ads)
    dp.register_message_handler(cancel, state="*", commands="отмена")
    dp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(update, lambda message: "Обновить базу данных" in message.text)
