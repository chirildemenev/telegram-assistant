import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.handlers import common, ai_chat, tasks
from bot.database import models  # Инициализация БД

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Подключаем роутеры
    dp.include_router(common.router)
    dp.include_router(tasks.router)
    dp.include_router(ai_chat.router)  # Последним - ловит все текстовые
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())