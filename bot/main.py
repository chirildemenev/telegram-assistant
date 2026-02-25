import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.handlers import common, ai_chat, tasks
from bot.database import models
import aiohttp
from aiohttp import web

logging.basicConfig(level=logging.INFO)

# Fake health check server для Render
async def health_check(request):
    return web.Response(text="OK")

async def start_health_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
    logging.info("Health check server started on port 10000")

async def main():
    # Запускаем health check
    asyncio.create_task(start_health_server())
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(common.router)
    dp.include_router(tasks.router)
    dp.include_router(ai_chat.router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
