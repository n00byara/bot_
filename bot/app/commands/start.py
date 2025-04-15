from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message as AMessage

from database import db
from text import Message

start = Router(name=__name__)

@start.message(CommandStart())
async def cmd_start(message: AMessage):
    user = db.get_user(message.from_user.id, message.from_user.username)

    if user.role_id != 1:
        return await message.answer(f"админ")

    return await message.answer(text=Message.BOT_START_USER.value)