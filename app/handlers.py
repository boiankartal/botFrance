from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

router = Router()
import app.keyboards as kb


@router.message(CommandStart)
async def start(message: Message):
    await message.answer("Добро пожаловать")
