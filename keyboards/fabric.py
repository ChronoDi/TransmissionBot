from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from lexicon import lexicon


def get_reply_keyboard(names: list[str], width: int = 2, is_one_time: bool = True) -> ReplyKeyboardMarkup:
    buttons: list[KeyboardButton] = []
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    for name in names:
        buttons.append(KeyboardButton(text=name))

    builder.row(*buttons, width=width)

    return builder.as_markup(on_time_keyboard=is_one_time, resize_keyboard=True)
