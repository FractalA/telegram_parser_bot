from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1: KeyboardButton = KeyboardButton("Обновить базу данных")
b2: KeyboardButton = KeyboardButton("Вывести все объявления")
b3: KeyboardButton = KeyboardButton("Вывести новые")
b4: KeyboardButton = KeyboardButton("Выбрать кол-во объявлений")

kb_client: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1, b2, b3, b4)
