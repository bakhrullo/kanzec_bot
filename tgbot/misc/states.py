from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStartState(StatesGroup):
    get_name = State()
    get_contact = State()


class UserMenuState(StatesGroup):
    get_cat = State()
    get_prod_type = State()
    get_prod = State()
    get_conf = State()
