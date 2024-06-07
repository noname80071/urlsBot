import aiohttp
import asyncio

async def check_telegram_user(username):
    token = '6697556330:AAEt5MP1RixQ8--rl9Z3IRip97Ojekax4Kw'
    base_url = f'https://api.telegram.org/bot{token}/'
    method = 'getChat'

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url + method, params={'chat_id': username}) as response:
            data = await response.json()
            return data.get('ok', False)

async def main():
    username = 'siberiaa'
    user_exists = await check_telegram_user(username)
    if user_exists:
        print(f'Пользователь Telegram с ником @{username} существует')
    else:
        print(f'Пользователь Telegram с ником @{username} не существует')

if __name__ == '__main__':
    asyncio.run(main())