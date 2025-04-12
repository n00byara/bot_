from dataclasses import dataclass
from typing import Any

from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene
from aiogram.fsm.scene import on
from aiogram.types import Message as AMessage
from aiogram.types import ReplyKeyboardRemove

from database import db
from keyboards import marks_kb
from text import Message
from quiz import Quiz as QuizState

@dataclass
class Question:
    text: str

QUESTIONS = [
    Message.QUIZ_QUESTION_1.value,
    Message.QUIZ_QUESTION_2.value,
    Message.QUIZ_QUESTION_3.value,
    Message.QUIZ_QUESTION_4.value,
    Message.QUIZ_QUESTION_5.value,
    Message.QUIZ_QUESTION_6.value
]

# Сцена проведения мероприятия
class Quiz(Scene, state="quiz"):
    @on.message.enter()
    async def on_enter(self, message: AMessage, state: FSMContext, step: int | None = 0) -> Any:
        await state.update_data(step=step)

        if not QuizState.state():
            return await self.wizard.exit()

        if db.check_user_from_quiz(message.chat.username, QuizState.id()):
            return await self.wizard.exit()

        try:
            quiz = QUESTIONS[step]
        except IndexError:
            return await self.wizard.exit()

        match(step):
            case 1 | 2 | 3:
                await message.answer(text=QUESTIONS[step], reply_markup=marks_kb)
            case _:
                await message.answer(text=QUESTIONS[step], reply_markup=ReplyKeyboardRemove())

    @on.message.exit()
    async def on_exit(self, message: AMessage, state: FSMContext) -> None:
        repeat = db.check_user_from_quiz(message.chat.username, QuizState.id())
        if repeat:
            await message.answer(text=Message.QUIZ_REPEAT_ERROR.value)

        if QuizState.state() and not repeat:
            user = db.get_user(message.chat.username)

            data = await state.get_data()
            answers = data.get("answers", [])

            for i in range(1, 4):
                db.add_quiz_answers(answers[i], i, user.id, QuizState.id())

            await message.answer(text=Message.QUIZ_RESULT.value)
        elif not QuizState.state() and not repeat:
            await message.answer(text=Message.QUIZ_START_ERROR.value)
        await state.set_data({})

    @on.message(F.text)
    async def answer(self, message: AMessage, state: FSMContext) -> None:
        data = await state.get_data()
        step = data["step"]
        
        answers = data.get("answers", [])
        answers.append(message.text)

        await state.update_data(answers=answers)
        await self.wizard.retake(step=step + 1)

quiz_router = Router(name=__name__)
quiz_router.message.register(Quiz.as_handler(), Command("go"))