from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()
import app.keyboards as kb
import app.database.requests as rq


# FSM состояние
class Add_cours(StatesGroup):
    name = State()
    description = State()
    img_id = State()
    price = State()
    active = State()
    online_or_record = State()


@router.message(Command("start"))
async def start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer("Добро пожаловать")
    await main(message)


async def main(message):
    await message.answer(text="🥖 Главное меню", reply_markup=kb.main)


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


@router.callback_query(F.data.startswith("cours_"))
async def get_courses(callback: CallbackQuery):
    id_cours = callback.data.split("_")[1]
    cours = await rq.get_cours(id_cours)
    await callback.message.answer_photo(
        photo=cours.img_tg_id,
        caption=f"Имя:{cours.name}\nОписание:\n{cours.description}",
    )
