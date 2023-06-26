from aiogram.filters.state import State, StatesGroup


class FSMTransmission(StatesGroup):
    menu = State()
    download = State()
    look_files = State()
    take_url_file = State()
    delete_select_file = State()
    delete_accept = State()
    move_select_file = State()
    move_select_folder = State()
    move_accept = State()
