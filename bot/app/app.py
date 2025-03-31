from aiogram import Bot, Dispatcher
from configuration import config

bot = Bot(token=config.token)
dp = Dispatcher()

async def start():
    await dp.start_polling(bot)