import asyncio
from os import getenv

import matplotlib.pyplot as plt
from aiogram import (Bot,
                     Dispatcher,
                     F)
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiohttp import ClientSession
from .keyboards.reply_keyboards import main_menu_keyboerd


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
        "category": []
    }
    print("*" * 80)
    print(data)
    async with ClientSession() as session:
        async with session.post(f"{BACKEND_URL}/create_user", json=data) as response:
            if response.status == 201:
                await message.reply("The registration went through automatically, now you can use the bot", reply_markup=main_menu_keyboerd())
            else:
                await message.answer(f"Error {response.status, response.text}")


@dp.message(F.text == "Add Category")
async def add_category(message: Message):
    if message.text:
        data = {
            "title": message.text,
            "user_id": message.from_user.id
        }
        print(data)
        print("*" * 80)
        async with ClientSession() as session:
            async with session.post(f'{BACKEND_URL}/create_category', json=data) as response:
                if response.status == 201:
                    await message.answer("Okey")

@dp.message(F.text == "Get All")
async def get_all(message: Message):
    data = {
        "user_id":  message.from_user.id
    }
    print(data)
    print("!" * 80)
    async with ClientSession() as session:
        async with session.get(f"{BACKEND_URL}/get_all_categories", json=data) as response:
            if response.status == 200:
                await message.answer(f"Here {response.json()}")



async def start() -> None:
    await dp.start_polling(bot)

