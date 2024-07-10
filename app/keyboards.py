from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
)
import app.database.request as rq
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Обучение", callback_data="study")],
        [InlineKeyboardButton(text="Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="Поддержка", callback_data="support")],
    ]
)

study = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Индивидуальные занятия", callback_data="individual"
            )
        ],
        [InlineKeyboardButton(text="Онлайн курсы", callback_data="cours")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_menu")],
    ]
)

main_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Курсы", callback_data="cours_admin")],
    ]
)


async def get_courses_admin():
    all_courses = await rq.get_courses_admin()
    keyboard = InlineKeyboardBuilder()
    if all_courses:
        for cours in all_courses:
            keyboard.add(
                InlineKeyboardButton(
                    text=cours.name, callback_data=f"coursAdmin_{cours.id}"
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


async def buy_cours(id):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Купить", callback_data=f"buy_cours_{id}"),
    )
    keyboard.add(
        InlineKeyboardButton(text="Назад", callback_data="back"),
    )
    return keyboard.adjust(1).as_markup()


async def edit_list(id, message_id):
    keyboard = InlineKeyboardBuilder()
    cours = await rq.get_cours(id)
    keyboard.add(
        InlineKeyboardButton(text="Изменить название", callback_data=f"editName_{id}"),
        InlineKeyboardButton(
            text="Изменить описание", callback_data=f"editDescription_{id}"
        ),
        InlineKeyboardButton(text="Изменить цену", callback_data=f"editPrice_{id}"),
        InlineKeyboardButton(
            text=f"Активный: {cours.active}",
            callback_data=f"editActive_{id}",
        ),
        InlineKeyboardButton(text="Удалить курс", callback_data=f"delete_cours_{id}"),
    )
    keyboard.add(
        InlineKeyboardButton(text="Назад", callback_data="back"),
    )
    return keyboard.adjust(1).as_markup()


back = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back")]]
)
