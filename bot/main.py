import asyncio
from os import getenv

from aiogram import (Bot,
                     Dispatcher,
                     F)
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession

from .keyboards.reply_keyboards import main_menu_keyboard, categories_keyboard
from .utils import Category


BOT_TOKEN = getenv("BOT_TOKEN")
BACKEND_URL = getenv("BACKEND_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hi, {message.from_user.full_name}!")
    print(message.from_user)
    data = {
        "telegram_id": message.from_user.id,
        "name": message.from_user.username,
        "category": [],
    }
    async with ClientSession() as session:
        async with session.post(f"{BACKEND_URL}/create_user", json=data) as response:
            text = await response.text()
            if response.status == 201:
                await message.reply(
                    "The registration went through automatically, now you can use the bot",
                    reply_markup=main_menu_keyboard(),
                )
            else:
                await message.answer(f"Error {response.status, text}")


@dp.message(F.text == "Add Category")
async def add_category(message: Message, state: FSMContext):
    await state.set_state(Category.category_input)
    await message.reply("Enter category name: ")


@dp.message(Category.category_input)
async def add_category(message: Message, state: FSMContext):
    if message.text:
        data = {
            "title": message.text,
            "telegram_id": message.from_user.id,
            "amount": 0.0,
            "total": 0.0
        }
        async with ClientSession() as session:
            async with session.post(
                f"{BACKEND_URL}/create_category", json=data
            ) as response:
                if response.status == 201:
                    await message.answer("Okey")
    await state.clear()


@dp.message(F.text == "Get All")
async def get_all(message: Message):
    data = {"telegram_id": message.from_user.id}
    async with ClientSession() as session:
        async with session.get(
            f"{BACKEND_URL}/get_all_categories", json=data
        ) as response:
            if response.status == 200:
                response_data = await response.json()
                all_categories = [i.get("title") for i in response_data]
                keyboard = categories_keyboard(all_categories)
                await message.answer(f"Here", reply_markup=keyboard)


@dp.message(F.text == "To Main Keyboard")
async def return_to_main_kb(message: Message):
    await message.answer("Goodbye", reply_markup=main_menu_keyboard())


async def start() -> None:
    await dp.start_polling(bot)
