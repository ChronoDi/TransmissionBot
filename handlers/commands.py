from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters.admins import IsAdmin
from lexicon import lexicon
from keyboards.fabric import get_reply_keyboard

router: Router = Router()
router.message.filter(IsAdmin())


async def process_start_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=lexicon['start'], reply_markup=get_reply_keyboard(names=[lexicon['transmission']]))


def process_all_command() -> None:
    router.message.register(process_start_command, CommandStart())


process_all_command()
