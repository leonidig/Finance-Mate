from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text="Add Category")
    builder.button(text="Get All")
    builder.button(text="Category Chart")
    builder.button(text="Chart By Total")
    builder.button(text="Delete Category")
    builder.button(text="Total spent")

    return builder.as_markup()