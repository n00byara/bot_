from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message as AMessage

from database import db
from keyboards import create_quiz_kb
from quiz import Quiz
from text import Message

start_quiz = Router(name=__name__)

@start_quiz.message(Command("start_quiz"))
async def start(message: AMessage):
    user = db.get_user(message.chat.username)
    quiz = db.get_quiz()

    if user.role_id != 3 or quiz.teacher_id == user.id:
        if Quiz.state():
            await message.answer(f"Мероприятие \"{quiz.name}\" уже идет")
        elif quiz:
            Quiz.start(quiz.id)
            await message.answer(f"Мероприятие \"{quiz.name}\" запущено")

stop_quiz = Router(name=__name__)

@stop_quiz.message(Command("stop_quiz"))
async def stop(message: AMessage):
    user = db.get_user(message.chat.username)
    quiz = db.get_quiz()

    if user.role_id != 3 or quiz.teacher_id == user.id:
        Quiz.stop()

        await message.answer(f"Мероприятие \"{quiz.name}\" остановлено")

create_quiz = Router(name=__name__)

@create_quiz.message(Command("create_quiz"))
async def start(message: AMessage):
    role = db.get_role(message.chat.username)

    if role.id == 1:
        await message.answer(Message.QUIZ_TYPE.value, reply_markup=create_quiz_kb)

create_excel = Router(name=__name__)

@create_excel.message(Command("create_excel"))
async def get(message: AMessage):
    answers = db.get_quiz_result()
    
    for answer in answers:
        await message.answer(text=f"student = {answers.student}, teacher = {answers.teacher}")