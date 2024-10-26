from aiogram.fsm.state import State, StatesGroup



class Category(StatesGroup):
    category_input = State()


class Transaction(StatesGroup):
    transaction_input = State()