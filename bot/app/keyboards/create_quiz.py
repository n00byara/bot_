from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup

from text import Message

kb_list = [
    [
        KeyboardButton(text=Message.GAME_BUTTON.value),
        KeyboardButton(text=Message.QUIZ_BUTTON.value),
        KeyboardButton(text=Message.OTHER_BUTTON.value)
    ]
]

create_quiz_kb = ReplyKeyboardMarkup(
    keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True
)