from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

router = Router()
import app.keyboards as kb
import app.database.requests as rq

url_bot = "https://t.me/frantessstbot"


# FSM состояние
class Add_cours(StatesGroup):
    name = State()
    description = State()
    img_id = State()
    price = State()
    active = State()
    online_or_record = State()


class editName(StatesGroup):
    new_name = State()
    id = State()
    callback = State()


class editDescription(StatesGroup):
    new_description = State()
    id = State()
    callback = State()


class editPrice(StatesGroup):
    new_price = State()
    id = State()
    callback = State()


@router.message(Command("start"))
async def start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer("Добро пожаловать")

    await main(message)
    if "coursID" in message.text:
        id = message.text.split("_")[1]
        await get_url_cours(id, message)


async def get_url_cours(id, message):
    id_cours = id
    cours = await rq.get_cours(id_cours)
    if cours.online_or_record == "Онлайн":
        text = f"После покупки курса вы получите доступ к группе, где вы будете:\n 1. Общаться с репетитором\n 2. Получать материалы, которые используются на занятиях\n 3. ...."
    if cours.online_or_record == "Запись":
        text = f"После покупки вы получите архив с курсом"

    await message.answer_photo(
        photo=cours.img_tg_id,
        caption=f"*Информация о курсе*\n\n*Название:* {cours.name}\n\n*Описание:*\n{cours.description}\n\n*Онлайн/Запись:* {cours.online_or_record}\n\n*Цена:* {cours.price}р \n\n`{text}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=await kb.buy_cours(cours.id),
    )


async def main(message):
    await message.answer(text="🥐 Главное меню", reply_markup=kb.main)


@router.callback_query(F.data == "cours")
async def get_courses(callback: CallbackQuery):
    await callback.message.answer(
        "Список доступных курсов", reply_markup=await kb.get_courses()
    )


@router.message(Command("admin_123"))
async def admin_menu(message: Message):
    await message.answer("Меню админа", reply_markup=kb.main_admin)


@router.callback_query(F.data == "cours_admin")
async def get_courses_admin(callback: CallbackQuery):
    await callback.message.answer(
        "Доступные курсы", reply_markup=await kb.get_courses_admin()
    )


@router.callback_query(F.data == "back")
async def cmd_back(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data == "add_cours")
async def add_cours(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(Add_cours.name)
    await callback.message.answer("Введите название курса", reply_markup=kb.otmena)


@router.message(Add_cours.name)
async def add_cours_discriprion(message: Message, state: FSMContext):
    if message.text == "Сбросить":
        await state.clear()
        await message.answer(
            "Регистрация курса отменена, чтобы начать заново введите /admin_123",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await state.update_data(name=message.text)
        await state.set_state(Add_cours.description)
        await message.answer("Введите описание курса", reply_markup=kb.otmena)


@router.message(Add_cours.description)
async def add_cours_descriprion(message: Message, state: FSMContext):
    if message.text == "Сбросить":
        await state.clear()
        await message.answer(
            "Регистрация курса отменена, чтобы начать заново введите /admin_123",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await state.update_data(description=message.text)
        await state.set_state(Add_cours.img_id)
        await message.answer("Пришлите превью курса (фото)", reply_markup=kb.otmena)


@router.message(Add_cours.img_id)
async def add_cours_discriprion(message: Message, state: FSMContext):
    if message.text == "Сбросить":
        await state.clear()
        await message.answer(
            "Регистрация курса отменена, чтобы начать заново введите /admin_123",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await state.update_data(img_id=message.photo[-1].file_id)
        await state.set_state(Add_cours.price)
        await message.answer("Введите цену курса", reply_markup=kb.otmena)


@router.message(Add_cours.price)
async def add_cours_discriprion(message: Message, state: FSMContext):
    if message.text == "Сбросить":
        await state.clear()
        await message.answer(
            "Регистрация курса отменена, чтобы начать заново введите /admin_123",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await state.update_data(price=message.text)
        await state.set_state(Add_cours.active)
        await message.answer(
            "Будет ли курс сразу доступен для пользователя? Да/Нет",
            reply_markup=kb.cuors_active_or_not,
        )


@router.message(Add_cours.active)
async def add_cours_discriprion(message: Message, state: FSMContext):
    if message.text == "Сбросить":
        await state.clear()
        await message.answer(
            "Регистрация курса отменена, чтобы начать заново введите /admin_123",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await state.update_data(active=message.text)
        await state.set_state(Add_cours.online_or_record)
        await message.answer(
            "Будет ли курс в записи или онлайн? Запись/Онлайн",
            reply_markup=kb.cuors_online_or_record,
        )


@router.message(Add_cours.online_or_record)
async def add_cours_discriprion(message: Message, state: FSMContext):
    if message.text == "Сбросить":
        await state.clear()
        await message.answer(
            "Регистрация курса отменена, чтобы начать заново введите /admin_123",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await state.update_data(online_or_record=message.text)
        data = await state.get_data()
        status = await rq.set_new_cours(data)
        if status == 200:
            text = "Регистрация курса завершена"
        else:
            text = "Ошибка!!!"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())

    await admin_menu(message)


@router.callback_query(F.data.startswith("cours_"))
async def get_cours(callback: CallbackQuery):
    id_cours = callback.data.split("_")[1]
    cours = await rq.get_cours(id_cours)
    if cours.online_or_record == "Онлайн":
        text = f"После покупки курса вы получите доступ к группе, где вы будете:\n 1. Общаться с репетитором\n 2. Получать материалы, которые используются на занятиях\n 3. ...."
    if cours.online_or_record == "Запись":
        text = f"После покупки вы получите архив с курсом"

    await callback.message.answer_photo(
        photo=cours.img_tg_id,
        caption=f"*Информация о курсе*\n\n*Название:* {cours.name}\n\n*Описание:*\n{cours.description}\n\n*Онлайн/Запись:* {cours.online_or_record}\n\n*Цена:* {cours.price}р \n\n`{text}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=await kb.buy_cours(cours.id),
    )


@router.callback_query(F.data.startswith("coursAdmin"))
async def get_cours_admin(callback: CallbackQuery):
    id_cours = callback.data.split("_")[1]
    cours = await rq.get_cours(id_cours)
    url = url_bot + f"?start=coursID_{cours.id}"
    await callback.message.answer_photo(
        photo=cours.img_tg_id,
        caption=f"*Информация о курсе*\n\n*Название:* {cours.name}\n\n*Описание:*\n{cours.description}\n\n*Онлайн/Запись:* {cours.online_or_record}\n\n*Цена:* {cours.price}р\n\n*Ссылка на курс:*\n`{url}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=await kb.edit_list(cours.id, callback.message.message_id),
    )


@router.callback_query(F.data.startswith("editActive"))
async def editActive(callback: CallbackQuery):
    await rq.editActive(callback.data.split("_")[1])
    await callback.message.delete()
    await get_cours_admin(callback)


@router.callback_query(F.data.startswith("delete_cours"))
async def delete_cours(callback: CallbackQuery):
    await rq.delete_cours(callback.data.split("_")[2])
    await callback.message.delete()
    await callback.message.answer("Курс успешно удален!")
    await get_courses_admin(callback)


@router.callback_query(F.data.startswith("editName"))
async def editName_1(callback: CallbackQuery, state: FSMContext):
    await state.set_state(editName.id)
    await state.update_data(id=callback.data.split("_")[1])
    await state.set_state(editName.callback)
    await state.update_data(callback=callback)
    await state.set_state(editName.new_name)
    await callback.message.answer("Напишите новое имя")


@router.message(editName.new_name)
async def editName_update(message: Message, state: FSMContext):
    await state.update_data(new_name=message.text)
    data = await state.get_data()
    await state.clear()
    status = await rq.editName(data["id"], data["new_name"])
    await message.answer("Успешно!!!")
    await get_courses_admin(data["callback"])


##########################################################################################
@router.callback_query(F.data.startswith("editDescription"))
async def editDescription_1(callback: CallbackQuery, state: FSMContext):
    await state.set_state(editDescription.id)
    await state.update_data(id=callback.data.split("_")[1])
    await state.set_state(editDescription.callback)
    await state.update_data(callback=callback)
    await state.set_state(editDescription.new_description)
    await callback.message.answer("Напишите новое описание курса")


@router.message(editDescription.new_description)
async def editDescription_update(message: Message, state: FSMContext):
    await state.update_data(new_description=message.text)
    data = await state.get_data()
    await state.clear()
    status = await rq.editDescription(data["id"], data["new_description"])
    await message.answer("Успешно!!!")
    await get_courses_admin(data["callback"])


#######################################################################################################
@router.callback_query(F.data.startswith("editPrice"))
async def editPrice_1(callback: CallbackQuery, state: FSMContext):
    await state.set_state(editPrice.id)
    await state.update_data(id=callback.data.split("_")[1])
    await state.set_state(editPrice.callback)
    await state.update_data(callback=callback)
    await state.set_state(editPrice.new_price)
    await callback.message.answer("Укажи новую цену")


@router.message(editPrice.new_price)
async def editPrice_update(message: Message, state: FSMContext):
    await state.update_data(new_price=message.text)
    data = await state.get_data()
    await state.clear()
    status = await rq.editPrice(data["id"], data["new_price"])
    await message.answer("Успешно!!!")
    await get_courses_admin(data["callback"])


@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):
    user = await rq.get_user(callback.message.chat.id)
    cours = await rq.get_cours(user.cours)
    if not cours:
        text = ""
    else:
        text = cours.name
    await callback.message.answer(
        f"*Ваш профиль*\n\n*Имя:* {callback.message.chat.full_name}\n\n*ID:* {user.tg_id}\n\n*Курс:* {text}",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb.back,
    )


@router.callback_query(F.data == "support")
async def support(callback: CallbackQuery):
    await callback.message.answer(
        "Свяжитесь с нами @pawwvw",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb.back,
    )
