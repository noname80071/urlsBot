from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import time
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from config import BOT_TOKEN as TOKEN
import kb
import states

router = Router()
bot = Bot(token=TOKEN)

is_running = False


@router.message(Command('start'))
async def start_handler(msg: Message):
    global is_running
    if not is_running:
        await msg.answer(text='Добро пожаловать!', reply_markup=kb.menu)
    else:
        await msg.answer(text='Бот уже работает')


@router.message(F.text == 'Загрузка базы')
async def load_base(msg: Message, state: FSMContext):
    await msg.answer(text='Загрузите файл')
    await state.set_state(states.SendFile.send_file)


@router.message(states.SendFile.send_file)
async def start_selection(msg: Message, state: FSMContext):
    try:
        await state.clear()
        await state.update_data(file_name=msg.document.file_name)
        file_name = msg.document.file_name
        await msg.answer(text='Идет загрузка базы...', reply_markup=kb.menu)
        file = await bot.get_file(msg.document.file_id)
        file_path = file.file_path
        await bot.download_file(file_path, file_name)
        with open(file_name) as f:
            file_size = len(f.read().split())
            f.close()
        time.sleep(1)
        await msg.answer(text=f'Загружено {file_size} ссылок', reply_markup=kb.menu)
        time.sleep(1)
        await msg.answer(text='Операция завершена', reply_markup=kb.menu)
    except Exception as e:
        print(e)
        await msg.answer(text=f'Неверный формат.')


@router.message(F.text == 'Начать поиск')
async def start_search(msg: Message, state: FSMContext):
    await msg.answer(text='Поиск начат.', reply_markup=kb.stop)
    await asyncio.create_task(check_urls(msg, state))


async def check_url(session, url, msg: Message, is_running: bool):
    st_accept = "text/html"
    st_useragent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15")
    headers = {
        "Accept": st_accept,
        "User-Agent": st_useragent
    }
    if is_running:
        try:
            async with session.get(url, headers=headers) as response:
                src = await response.text()
                if 'tgme_page_title' not in src:
                    await msg.answer(f'Ссылка {url} не работает')

        except aiohttp.ClientError as e:
            print(e)
    else:
        return


async def check_urls(msg: Message, state: FSMContext):
    global is_running
    data = await state.get_data()
    file_name = data['file_name']
    is_running = True

    async with aiohttp.ClientSession() as session:
        while True:
            if is_running:
                try:
                    start_time = time.time()
                    tasks = []
                    if is_running:
                        with open(file_name) as file:
                            if is_running:
                                for url in file:
                                    url = url.strip()
                                    tasks.append(check_url(session, url, msg, is_running))
                            else:
                                break

                    await asyncio.gather(*tasks)
                    end_time = time.time()
                    print(end_time - start_time)
                except FileNotFoundError as e:
                    print(f'Файл не найден: {e}')
                    break
            else:
                break


@router.message(F.text == 'Остановить')
async def stop(msg: Message):
    global is_running
    if is_running:
        is_running = False
        await msg.answer(text='Поиск остановлен', reply_markup=kb.menu)
    else:
        await msg.answer(text='Бот не работает')
