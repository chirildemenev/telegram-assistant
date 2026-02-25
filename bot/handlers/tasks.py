from aiogram import Router, types
from aiogram.filters import Command
from bot.database.queries import add_task, get_user_tasks, complete_task, delete_task

router = Router()

@router.message(Command("add"))
async def cmd_add(message: types.Message):
    """Добавить задачу"""
    text = message.text.replace("/add", "", 1).strip()
    
    if not text:
        await message.answer("❌ Напиши задачу после команды: /add Купить молоко")
        return
    
    task = add_task(message.from_user.id, text)
    await message.answer(f"✅ Задача добавлена: #{task.id}\n<i>{text}</i>", parse_mode="HTML")

@router.message(Command("list"))
async def cmd_list(message: types.Message):
    """Показать задачи"""
    tasks = get_user_tasks(message.from_user.id, only_active=True)
    
    if not tasks:
        await message.answer("📭 У тебя нет активных задач!\nДобавь: /add <текст>")
        return
    
    text = "📋 <b>Твои задачи:</b>\n\n"
    for i, task in enumerate(tasks, 1):
        text += f"{i}. {task.text}\n"
        text += f"   <i>ID: {task.id} | {task.created_at.strftime('%d.%m')}</i>\n\n"
    
    text += "Отметить выполненной: /done <ID>\nУдалить: /delete <ID>"
    await message.answer(text, parse_mode="HTML")

@router.message(Command("done"))
async def cmd_done(message: types.Message):
    """Отметить выполненной"""
    try:
        task_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.answer("❌ Укажи ID задачи: /done 5")
        return
    
    if complete_task(message.from_user.id, task_id):
        await message.answer(f"✅ Задача #{task_id} выполнена!")
    else:
        await message.answer("❌ Задача не найдена или уже выполнена")

@router.message(Command("delete"))
async def cmd_delete(message: types.Message):
    """Удалить задачу"""
    try:
        task_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.answer("❌ Укажи ID задачи: /delete 5")
        return
    
    if delete_task(message.from_user.id, task_id):
        await message.answer(f"🗑 Задача #{task_id} удалена")
    else:
        await message.answer("❌ Задача не найдена")