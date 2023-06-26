from aiogram import Router
from aiogram.types import Message

from filters.admins import IsAdmin
from lexicon import lexicon

router = Router()
router.message.filter(IsAdmin())


async def process_hello_message(message: Message):
    await message.answer(text=lexicon['admin_echo'])


def process_all_handlers():
    router.message.register(process_hello_message)


process_all_handlers()
