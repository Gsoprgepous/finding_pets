# -*- coding: utf-8 -*- 
"""Finding Pets Bot"""

from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from neural_network import analyze_image
from database import create_table, add_pet_to_db, get_found_pets, like_found_pet

TOKEN = 'хххх'
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

create_table()

@router.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="Я потерял питомца", callback_data="lost_pet"),
        InlineKeyboardButton(text="Я нашел питомца", callback_data="found_pet"),
        InlineKeyboardButton(text="Посмотреть фото найденных питомцев", callback_data="view_found_pets"),
        InlineKeyboardButton(text="Посмотреть фото потерянных питомцев", callback_data="view_lost_pets"),
        InlineKeyboardButton(text="Подобрать питомца из приюта", callback_data="shelter_pet"),
    ]
    keyboard.add(*buttons)
    await message.answer("Выберите действие:", reply_markup=keyboard)

@router.callback_query(lambda cb: cb.data == "lost_pet")
async def lost_pet(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Пожалуйста, прикрепите фото вашего потерянного питомца, добавьте описание и ваши контакты.")

@router.callback_query(lambda cb: cb.data == "found_pet")
async def found_pet(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Пожалуйста, прикрепите фото найденного питомца, добавьте описание и ваши контакты.")

@router.callback_query(lambda cb: cb.data == "view_found_pets")
async def view_found_pets(callback: types.CallbackQuery):
    await callback.answer()
    pets = get_found_pets()
    if not pets:
        await callback.message.answer("Нет найденных питомцев.")
        return

    for pet in pets:
        photo_path = pet[2]
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("👍", callback_data=f"like_{pet[0]}")
        )
        await callback.message.answer_photo(photo=photo_path, reply_markup=keyboard)

@router.callback_query(lambda cb: cb.data.startswith("like_"))
async def like_pet(callback: types.CallbackQuery):
    pet_id = int(callback.data.split("_")[1])
    like_found_pet(pet_id)
    await callback.answer("Спасибо за ваш лайк! Контакты владельца будут отправлены вам.")

@router.callback_query(lambda cb: cb.data == "view_lost_pets")
async def view_lost_pets(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Здесь будет список потерянных питомцев.")

@router.callback_query(lambda cb: cb.data == "shelter_pet")
async def shelter_pet(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Пожалуйста, напишите место и примерные координаты, прикрепите фото, добавьте описание и укажите ваши контакты.")

@router.message(lambda message: message.photo)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    photo_path = f"photos/{photo.file_id}.jpg"
    await photo.download(photo_path)

    breed = analyze_image(photo_path)
    add_pet_to_db(message.from_user.id, photo_path, breed)
    await message.reply(f"Распознанная порода: {breed}. Информация о питомце сохранена.")

async def main():
    print("Бот запущен")
    await dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

