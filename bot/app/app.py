from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.scene import SceneRegistry

from configuration import config
from commands import start as start_router
from commands import start_quiz as start_quiz_router
from commands import stop_quiz as stop_quiz_router
from commands import create_quiz as create_quiz_command_router
from commands import create_excel as create_excel_router
from scenes import CreateQuiz as CreateQuizScene
from scenes import create_quiz as create_quiz_scene_router
from scenes import Quiz as QuizScene
from scenes import quiz_router as quiz_scene_router

scenes = [CreateQuizScene, QuizScene]

bot = Bot(token=config.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.include_routers(
    start_router,
    start_quiz_router,
    stop_quiz_router,
    create_quiz_command_router,
    create_quiz_scene_router,
    create_excel_router,
    quiz_scene_router
)

scene_registry = SceneRegistry(dp)

for scene in scenes:
    scene_registry.add(scene)

async def start():
    await dp.start_polling(bot)