from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


menu = [[KeyboardButton(text='Загрузка базы'),
         KeyboardButton(text='Начать поиск')],
        [KeyboardButton(text='Перезапустить')]]
menu = ReplyKeyboardMarkup(keyboard=menu)

stop = [[KeyboardButton(text='Остановить')]]
stop = ReplyKeyboardMarkup(keyboard=stop)
