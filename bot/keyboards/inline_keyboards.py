from aiogram.utils.keyboard import InlineKeyboardBuilder


def transaction_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Enter Transaction", callback_data="enter_transaction")


    return builder.as_markup()


def categories_keyboard(categories):
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(text=category, callback_data=f"category_{category}")
    
    builder.adjust(1)
    return builder.as_markup()
