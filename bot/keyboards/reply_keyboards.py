from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text="Add Category")
    builder.button(text="Get All")
    builder.button(text="Category Chart")
<<<<<<< HEAD
    builder.button(text="Chart By Total")
=======
    builder.button(text="Chart by total")
>>>>>>> 01be670db25303917b43e4c0b24677c0e8b2d9c4

    return builder.as_markup()



