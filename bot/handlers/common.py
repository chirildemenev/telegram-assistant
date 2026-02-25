from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я твой персональный ассистент.\n\n"
        "🤖 Режим ИИ: Просто пиши мне что угодно - я отвечу через Gemini\n"
        "📝 Задачи:\n"
        "/add текст - добавить задачу\n"
        "/list - список задач\n"
        "/done номер - отметить выполненной\n"
        "/delete номер - удалить задачу\n\n"
        "🧠 Управление:\n"
        "/clear - очистить историю диалога\n"
        "/plan - проанализировать мои задачи"
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await cmd_start(message)