
from dataclasses import dataclass, field
from typing import Any

from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene
from aiogram.fsm.scene import on
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove

from database import db
from text import Message

@dataclass
class Question:
    text: str

QUESTIONS = [
    Message.QUIZ_CREATE_QUESTION_1.value,
    Message.QUIZ_CREATE_QUESTION_2.value,
    Message.QUIZ_CREATE_QUESTION_3.value,
    Message.QUIZ_CREATE_QUESTION_4.value
]

# Сцена создания мероприятия
class CreateQuiz(Scene, state="create_quiz"):
    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext, step: int | None = 0) -> Any:
        await state.update_data(step=step)

        data = await state.get_data()
        step = data["step"]
        answers = data.get("answers", [])
        answers.append(message.text)
        await state.update_data(answers=answers)
        
        try:
            quiz = QUESTIONS[step]
        except IndexError:
            return await self.wizard.exit()

        return await message.answer(
            text=QUESTIONS[step],
            reply_markup=ReplyKeyboardRemove()
        )

    @on.message.exit()
    async def on_exit(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        answers = data.get("answers", [])

        quiz = db.create_quiz(answers)
        await message.answer(text=f"{Message.QUIZ_ADD_SUCCESS.value}: {quiz.id}")

        await state.set_data({})

    @on.message(F.text)
    async def answer(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        step = data["step"]

        if step == 3:
            user = db.find_user(message.text)
            if not user:
                QUESTIONS[3] = Message.QUIZ_FIND_USER_ERROR.value
                return await self.wizard.retake(step=step)

        await self.wizard.retake(step=step + 1)


create_quiz = Router(name=__name__)
# Обработчик кнопок 1 из 3 типов мероприятия
create_quiz.message.register(
    CreateQuiz.as_handler(),
    F.text == Message.GAME_BUTTON.value or F.text == Message.OTHER_BUTTON.value or Message.QUIZ_BUTTON.value
)