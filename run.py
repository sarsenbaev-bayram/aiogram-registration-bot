import asyncio
import logging

import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from config import TOKEN
from apps.handlers import router
from apps.database import init_db
load_dotenv

TOKEN = os.getenv("BOT_TOKEN")
dp = Dispatcher()

async def main():
    init_db()
    dp.include_router(router)
    await dp.start_polling(bot)
     

if __name__ == "__main__":  
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")






