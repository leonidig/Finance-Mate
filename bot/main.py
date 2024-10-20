import asyncio
from os import getenv

import matplotlib.pyplot as plt
from aiogram import (Bot,
                     Dispatcher)
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiohttp import ClientSession


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
        "name": message.from_user.username
    }
    print("*" * 80)
    print(data)
    async with ClientSession() as session:
        async with session.post(f"{BACKEND_URL}/create_user", json=data) as response:
            if response.status == 201:
                await message.reply("The registration went through automatically, now you can use the bot")
            else:
                await message.answer(f"Error {response.status, response.text}")


async def start() -> None:
    await dp.start_polling(bot)

