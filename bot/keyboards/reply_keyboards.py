from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_keyboerd():
    builder = ReplyKeyboardBuilder()

    builder.button(text="Add Category")
    builder.button(text="Get All")

    return builder.as_markup()