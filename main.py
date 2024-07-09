import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
import os
from app.handlers import router
from aiogram.filters import CommandStart, Command
from app.database.models import async_main
import app.database.request as rq
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
import app.keyboards as kb
from aiogram.enums import ParseMode

bot = Bot(token=os.getenv("TOKEN"))


async def main():
    dp = Dispatcher()
    load_dotenv()
    await async_main()
    dp.include_router(router)
    await dp.start_polling(bot)


class Broadcast(StatesGroup):
    text = State()


class Broadcast_photo(StatesGroup):
    text = State()
    media = State()


@router.message(Command("broadcasts"))
async def broadcast_start(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv("admin_id_1")):
        await state.set_state(Broadcast.text)
        await message.answer("Пришли сообщение без медиа", reply_markup=kb.otmena)


@router.message(Broadcast.text)
async def broadcast(message: Message, state: FSMContext):
    if message.text == "Сбросить":
        await state.clear()
        await message.answer("Рассылка отменена", reply_markup=ReplyKeyboardRemove())
    else:
        await state.update_data(text=message.text)
        data = await state.get_data()
        users = await rq.get_users()
        await state.clear()
        await message.answer("Рассылка началась", reply_markup=ReplyKeyboardRemove())
        for user in users:
            try:
                await bot.send_message(
                    chat_id=user.tg_id,
                    text=f"{data['text']}",
                    parse_mode=ParseMode.MARKDOWN,
                )
            except:
                continue


######################################################################################


@router.message(Command("broadcasts_photo"))
async def broadcast_photo_start(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv("admin_id_1")):
        await state.set_state(Broadcast_photo.media)
        await message.answer("Пришли фото", reply_markup=kb.otmena)


@router.message(Broadcast_photo.media)
async def broadcast_photo_1(message: Message, state: FSMContext):
    if message.text == "Сбросить":
        await state.clear()
        await message.answer("Рассылка отменена", reply_markup=ReplyKeyboardRemove())
    else:
        await state.update_data(media=message.photo[-1].file_id)
        await state.set_state(Broadcast_photo.text)
        await message.answer("Пришли подпись к фото", reply_markup=kb.otmena)


@router.message(Broadcast_photo.text)
async def broadcast_photo_2(message: Message, state: FSMContext):
    if message.text == "Сбросить":
        await state.clear()
        await message.answer("Рассылка отменена", reply_markup=ReplyKeyboardRemove())
    else:
        await state.update_data(text=message.text)
        data = await state.get_data()
        users = await rq.get_users()
        await state.clear()
        await message.answer("Рассылка началась", reply_markup=ReplyKeyboardRemove())
        for user in users:
            try:
                await bot.send_photo(
                    chat_id=user.tg_id,
                    photo=data["media"],
                    caption=f"{data['text']}",
                    parse_mode=ParseMode.MARKDOWN,
                )
            except:
                continue


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
