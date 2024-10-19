import asyncio
import os
import matplotlib.pyplot as plt
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile, InputMediaPhoto


# Токен вашего Telegram бота
API_TOKEN = '7421304149:AAFMYRodAdTtd4WzurfRmxZ-tjAoLLw3MwY'


bot = Bot(token=API_TOKEN)
dp = Dispatcher()


def create_expense_chart(data):
    categories = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(6, 4))
    plt.bar(categories, values, color='skyblue')
    plt.xlabel('Categories')
    plt.ylabel('Sum')
    plt.title('All')
    plt.tight_layout()

    file_path = 'expense_chart.png'
    plt.savefig(file_path)
    plt.close()

    return file_path


@dp.message(Command("report"))
async def send_expense_report(message: types.Message):
    data = {
        'Food': 200,
        'Transport': 50,
        'Entertainment': 150,
        'Utilities': 100
    }

    # Создаем график
    file_path = create_expense_chart(data)

    photo1 = FSInputFile("expense_chart.png")
    await message.answer_photo(photo1, "Here")

    os.remove(file_path)

async def main() -> None:
    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())