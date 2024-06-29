from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

router = Router()
import app.keyboards as kb
import app.database.requests as rq


@router.message(CommandStart)
async def start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer("Добро пожаловать")
    await main(message)


async def main(message):
    await message.answer(text="🥖 Главное меню", reply_markup=kb.main)
