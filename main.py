import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from app.handlers import router
from app.database.models import async_main


async def main():
    dp = Dispatcher()
    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    await async_main()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
