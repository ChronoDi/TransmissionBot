from aiogram import Router
from aiogram.types import Message

from filters.admins import IsAdmin
from lexicon import lexicon
from services.logs import logging

router = Router()
router.message.filter(~IsAdmin())


async def process_message(message: Message):
    logging(f' id - {message.from_user.id},'
            f' username - {message.from_user.username},'
            f' first name - {message.from_user.first_name},'
            f' last name - {message.from_user.last_name}\n', is_error=True)

    await message.answer(lexicon['validate_error'])


def process_all_handlers() -> None:
    router.message.register(process_message)


process_all_handlers()
