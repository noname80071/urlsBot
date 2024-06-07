from aiogram.filters.state import StatesGroup, State


class SendFile(StatesGroup):
    send_file = State()


