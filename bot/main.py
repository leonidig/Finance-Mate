from os import (getenv,
                remove)
import asyncio

from aiogram import (Bot,
                     Dispatcher,
                     F)
from aiogram.filters import CommandStart
from aiogram.types import (Message,
                           CallbackQuery,
                           FSInputFile,
                           InputFile)
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession

from .keyboards.reply_keyboards import main_menu_keyboard
from .keyboards.inline_keyboards import (transaction_keyboard,
                                         categories_keyboard)
from .utils.states import (Category, 
                    Transaction,
                    Chart,
                    CategoryToDelete
                    )
from .utils.charts import (create_chart,
                           create_chart_by_total)


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


@dp.callback_query(F.data.startswith("category_"))
async def handle_category_selection(callback: CallbackQuery, state: FSMContext):
    selected_category = callback.data.split("_", 1)[1]
    await callback.answer()
    await callback.message.answer(f"You selected the category: {selected_category}")
    await callback.message.answer("What would you like to do?", reply_markup=transaction_keyboard())
    
    await state.update_data(selected_category=selected_category)



@dp.callback_query(F.data == "enter_transaction")
async def prompt_transaction_input(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Please enter the transaction amount:")
    await state.set_state(Transaction.transaction_input)


@dp.message(Transaction.transaction_input)
async def enter_transaction(message: Message, state: FSMContext):
    data = await state.get_data()
    selected_category = data.get("selected_category")

    if message.text:
        try:
            amount = float(message.text)
            transaction_data = {
                "category_title": selected_category,
                "telegram_id": message.from_user.id,
                "amount": amount
            }

            async with ClientSession() as session:
                async with session.post(f"{BACKEND_URL}/create_transaction", json=transaction_data) as response:
                    if response.status == 201:
                        await message.reply("Transaction recorded successfully.")
                    else: 
                        await message.answer(f"Error - {response.status}\nText - {await response.text()}")
        except ValueError:
            await message.reply("Please enter a valid amount.")
    await state.clear()


@dp.message(F.text == "Category Chart")
async def chart_answer(message: Message, state: FSMContext):
    await state.set_state(Chart.chart_name)
    await message.answer("Enter Category Name: ")


@dp.message(Chart.chart_name)
async def send_chart(message: Message, state: FSMContext):
    if message.text:
        data = {
            "telegram_id": message.from_user.id,
            "category_title": message.text
        }
        async with ClientSession() as session:
            async with session.get(f"{BACKEND_URL}/get_chart", json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    amounts = [t.get('amount') for t in result if t.get('amount') is not None]
                    if amounts:
                        chart_file = create_chart(amounts)
                        if chart_file:
                            photo = FSInputFile("chart.png")
                            await message.answer_photo(photo)
                        remove(chart_file)
    await state.clear()


@dp.message(F.text == "Chart By Total")
async def chart_by_total(message: Message):
    await message.reply("CUM")
    data = {
        "telegram_id": message.from_user.id
    }
    async with ClientSession() as session:
        async with session.get(f"{BACKEND_URL}/get_chart_by_total", json=data) as response:
            if response.status == 200:
                data = await response.json()
                if data:
                    chart_file = create_chart_by_total(data)
                    if chart_file:
                        try:
                            photo = FSInputFile(chart_file) 
                            await message.answer_photo(photo)
                        except Exception as e:
                            await message.reply(f"Error sending photo: {e}")
                        finally:
                            remove(chart_file)
            else:
                await message.reply(f"Code - {response.status}\nText - {await response.text()}")



@dp.message(F.text == "Delete Category")
async def enter_category(message: Message, state: FSMContext):
    await message.reply("Enter category name to delete: ")
    await state.set_state(CategoryToDelete.category_to_delete)


@dp.message(CategoryToDelete.category_to_delete)
async def delete_category(message: Message, state: FSMContext):
    categotry_name = message.text
    if categotry_name:
        data = {
            "category_title": categotry_name,
            "telegram_id": message.from_user.id
        }
        async with ClientSession() as session:
            async with session.delete(f"{BACKEND_URL}/delete_category/{categotry_name}", json=data) as response:
                if response.status == 200:
                    await message.answer("Okey")
                else:
                    await message.answer("Error")
    await state.clear()


async def start() -> None:
    await dp.start_polling(bot)