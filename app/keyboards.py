from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
import app.database.requests as rq
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Курсы", callback_data="cours")],
        [InlineKeyboardButton(text="Профиль", callback_data="cours")],
        [InlineKeyboardButton(text="Поддержка", callback_data="cours")],
    ]
)
