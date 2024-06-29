from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
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


main_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Курсы", callback_data="cours_admin")],
    ]
)


async def get_courses_admin():
    all_courses = await rq.get_courses()
    keyboard = InlineKeyboardBuilder()
    if all_courses:
        for cours in all_courses:
            keyboard.add(
                InlineKeyboardButton(
                    text=cours.name, callback_data=f"cours_admin_{cours.id}"
                )
            )
    keyboard.add(InlineKeyboardButton(text="+ Новый курс", callback_data="add_cours"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back"))
    return keyboard.adjust(1).as_markup()


cuors_active_or_not = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Нет")],
        [KeyboardButton(text="Да")],
        [KeyboardButton(text="Сбросить")],
    ]
)

cuors_online_or_record = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Запись")],
        [KeyboardButton(text="Онлайн")],
        [KeyboardButton(text="Сбросить")],
    ]
)

otmena = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сбросить")],
    ]
)


async def get_courses():
    all_courses = await rq.get_courses()
    keyboard = InlineKeyboardBuilder()
    if all_courses:
        for cours in all_courses:
            keyboard.add(
                InlineKeyboardButton(text=cours.name, callback_data=f"cours_{cours.id}")
            )
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back"))
    return keyboard.adjust(1).as_markup()
