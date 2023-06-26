from aiogram import Router
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.transmission import FSMTransmission
from utils.transmission.look_files import get_torrents_list
from keyboards.fabric import get_reply_keyboard
from lexicon import lexicon

look_files_router: Router = Router()


async def process_look_file(message: Message, state: FSMContext):
    await message.answer(text=get_torrents_list(),
                         reply_markup=get_reply_keyboard(names=[lexicon['delete'],
                                                                lexicon['move'],
                                                                lexicon['main_menu']]))
    await state.set_state(FSMTransmission.look_files)


async def wrong_id_input(message: Message):
    await message.answer(text=lexicon['torrent_wrong_input'])


def process_all_handlers() -> None:
    look_files_router.message.register(process_look_file, Text(text=lexicon['look_files']),
                                       StateFilter(FSMTransmission.menu))
    look_files_router.message.register(wrong_id_input,
                                       StateFilter(FSMTransmission.menu))
