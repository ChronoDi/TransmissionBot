from typing import Any
from aiogram import Router, F
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.transmission import FSMTransmission
from utils.transmission.look_files import try_get_torrent
from utils.transmission.delete import delete_torrent
from keyboards.fabric import get_reply_keyboard
from services.logs import logging
from lexicon import lexicon

delete_router: Router = Router()


async def process_delete_file(message: Message, state: FSMContext):
    await message.answer(text=lexicon['torrent_id'],
                         reply_markup=get_reply_keyboard(names=[lexicon['main_menu']]))
    await state.set_state(FSMTransmission.delete_select_file)


async def process_take_id_torrent(message: Message, state: FSMContext):
    torrent = try_get_torrent(int(message.text))

    if torrent:
        await state.update_data(torrent_id=torrent.id,
                                torrent_name=torrent.name)
        await message.answer(text=lexicon['torrent_delete_accept'].format(name=torrent.name),
                             reply_markup=get_reply_keyboard(names=[lexicon['yes'],
                                                                    lexicon['no'],
                                                                    lexicon['main_menu']]))
        await state.set_state(FSMTransmission.delete_accept)
    else:
        await message.answer(lexicon['torrent_not_found'],
                             reply_markup=get_reply_keyboard(names=[lexicon['main_menu']]))


async def wrong_id_input(message: Message):
    await message.answer(text=lexicon['torrent_wrong_input'])


async def process_final_delete_torrent(message: Message, state: FSMContext):
    temp_dict: dict[str: Any] = await state.get_data()
    torrent_id: int = temp_dict['torrent_id']
    torrent_name: str = temp_dict['torrent_name']
    delete_torrent(torrent_id)
    logging(f'File "{torrent_name}" delete by {message.from_user.username}')
    await state.clear()
    await message.answer(text=lexicon['torrent_file_removed'].format(name=torrent_name),
                         reply_markup=get_reply_keyboard(names=[lexicon['main_menu']]))


async def process_cancel_delete_torrent(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=lexicon['torrent_cancel_delete'],
                         reply_markup=get_reply_keyboard(names=[lexicon['main_menu']]))


def process_all_handlers() -> None:
    delete_router.message.register(process_delete_file, Text(text=lexicon['delete']),
                                   StateFilter(FSMTransmission.look_files))
    delete_router.message.register(process_take_id_torrent, F.text.isdigit(),
                                   StateFilter(FSMTransmission.delete_select_file))
    delete_router.message.register(process_final_delete_torrent, Text(text=lexicon['yes']),
                                   StateFilter(FSMTransmission.delete_accept))
    delete_router.message.register(process_cancel_delete_torrent, Text(text=lexicon['no']),
                                   StateFilter(FSMTransmission.delete_accept))
    delete_router.message.register(wrong_id_input,
                                   StateFilter(FSMTransmission.delete_select_file, FSMTransmission.delete_accept))
