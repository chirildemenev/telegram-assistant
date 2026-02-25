from aiogram import Router, types, F
from aiogram.filters import Command
from bot.services.gemini import gemini_service
from bot.database.queries import get_user_tasks

router = Router()

@router.message(Command("clear"))
async def cmd_clear(message: types.Message):
    gemini_service.clear_history(message.from_user.id)
    await message.answer("🧹 История диалога очищена!")

@router.message(Command("plan"))
async def cmd_plan(message: types.Message):
    """Проанализировать задачи через ИИ"""
    tasks = get_user_tasks(message.from_user.id, only_active=True)
    
    if not tasks:
        await message.answer("У тебя нет активных задач для анализа!")
        return
    
    tasks_text = "\n".join([f"{i+1}. {t.text}" for i, t in enumerate(tasks)])
    
    prompt = f"""У меня есть следующие задачи:
{tasks_text}

Помоги мне:
1. Расставить приоритеты (что срочное/важное)
2. Предложить порядок выполнения
3. Дать краткие советы по эффективности

Ответь структурированно и кратко."""
    
    await message.answer("🤔 Анализирую твои задачи...")
    
    response = await gemini_service.chat(message.from_user.id, prompt)
    await message.answer(response)

@router.message(F.text, ~F.text.startswith('/'))
async def ai_chat(message: types.Message):
    """Обычный диалог с ИИ — только если не команда"""
    await message.bot.send_chat_action(message.chat.id, "typing")
    
    response = await gemini_service.chat(message.from_user.id, message.text)
    await message.answer(response)