from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text="Add Category")
    builder.button(text="Get All")

    return builder.as_markup()



def categories_keyboard(categories):
    builder = ReplyKeyboardBuilder()
    builder.button(text="To Main Keyboard")
    for category in categories:
        builder.button(text=category)
    
    return builder.as_markup()