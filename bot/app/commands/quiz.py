from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message as AMessage
from aiogram.types import FSInputFile

from database import db
from excel import create_excel_from_dict_list
from excel import remove_file
from keyboards import create_quiz_kb
from quiz import Quiz
from text import Message

start_quiz = Router(name=__name__)

@start_quiz.message(Command("start_event"))
async def start(message: AMessage):
    user = db.get_user(message.from_user.id)
    quiz = db.get_quiz()

    if user.role_id != 3 or quiz.teacher_id == user.id:
        if Quiz.state():
            await message.answer(f"Мероприятие \"{quiz.name}\" уже идет")
        elif quiz:
            Quiz.start(quiz.id)
            await message.answer(f"Мероприятие \"{quiz.name}\" запущено")

stop_quiz = Router(name=__name__)

@stop_quiz.message(Command("stop_event"))
async def stop(message: AMessage):
    user = db.get_user(message.from_user.id)
    quiz = db.get_quiz()

    if user.role_id != 3 or quiz.teacher_id == user.id:
        Quiz.stop()

        await message.answer(f"Мероприятие \"{quiz.name}\" остановлено")
        answers = db.get_quiz_result()

        quiz_name = "имя_тренинга"
        date = "15.04.2025"
        file_name = f"Отчет_{date}_{quiz_name}.xlsx"
        file_path = create_excel_from_dict_list(answers, file_name)
        document = FSInputFile(file_path)
        await message.answer_document(document=document)
        remove_file(file_path)

create_quiz = Router(name=__name__)

@create_quiz.message(Command("create_event"))
async def start(message: AMessage):
    role = db.get_role(message.chat.username)

    if role.id == 1:
        await message.answer(Message.QUIZ_TYPE.value, reply_markup=create_quiz_kb)

create_excel = Router(name=__name__)

@create_excel.message(Command("create_excel"))
async def get(message: AMessage):
    answers = db.get_quiz_result()

    file_path = create_excel_from_dict_list(answers, "report.xlsx")
    document = FSInputFile(file_path)
    await message.answer_document(document=document)
    remove_file(file_path)