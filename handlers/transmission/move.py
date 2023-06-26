from typing import Any
from aiogram import Router, F
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from transmission_rpc import Torrent

from services.logs import logging
from services.process_folder import get_name
from states.transmission import FSMTransmission
from utils.transmission.look_files import try_get_torrent
from utils.transmission.move import move_torrent
from keyboards.fabric import get_reply_keyboard
from lexicon import lexicon
from config_data import config

move_router: Router = Router()


async def process_move_file(message: Message, state: FSMContext):
    await message.answer(text=lexicon['torrent_id'],
                         reply_markup=get_reply_keyboard(names=[lexicon['main_menu']]))
    await state.set_state(FSMTransmission.move_select_file)


async def process_take_id_torrent(message: Message, state: FSMContext):
    torrent = try_get_torrent(int(message.text))
    if torrent:
        await state.update_data(torrent=torrent)

        await message.answer(text=lexicon['select_folder'],
                             reply_markup=get_reply_keyboard(names=[lexicon['films'],
                                                                    lexicon['serials'],
                                                                    lexicon['another'],
                                                                    lexicon['main_menu']], width=3))
        await state.set_state(FSMTransmission.move_select_folder)
    else:
        await message.answer(lexicon['torrent_not_found'],
                             reply_markup=get_reply_keyboard(names=[lexicon['main_menu']]))


async def process_move_select_folder(message: Message, state: FSMContext):
    await state.update_data(folder=get_name(message.text))
    temp_dict: dict[str: Any] = await state.get_data()
    torrent: Torrent = temp_dict['torrent']

    if torrent.download_dir[-1] != get_name(message.text):
        await message.answer(text=lexicon['torrent_move_accept'].format(name=torrent.name, dir=message.text),
                             reply_markup=get_reply_keyboard(names=[lexicon['yes'],
                                                                    lexicon['no'],
                                                                    lexicon['main_menu']]))
        await state.set_state(FSMTransmission.move_accept)

    else:
        await message.answer(lexicon['torrent_here'])


async def wrong_id_input(message: Message):
    await message.answer(text=lexicon['torrent_wrong_input'])


async def process_final_move_torrent(message: Message, state: FSMContext):
    temp_dict: dict[str: Any] = await state.get_data()
    torrent = temp_dict['torrent']
    path = temp_dict['folder']
    move_torrent(torrent, path)
    logging(f'File "{torrent.name}" moved to folder {config.transmission.download_folder}{path} '
            f'by {message.from_user.username}')
    await state.clear()
    await message.answer(text=lexicon['torrent_file_moved'].format(name=torrent.name),
                         reply_markup=get_reply_keyboard(names=[lexicon['main_menu']]))


async def process_cancel_move_torrent(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=lexicon['torrent_cancel_move'],
                         reply_markup=get_reply_keyboard(names=[lexicon['main_menu']]))


def process_all_handlers() -> None:
    move_router.message.register(process_move_file, Text(text=lexicon['move']),
                                 StateFilter(FSMTransmission.look_files))
    move_router.message.register(process_take_id_torrent, F.text.isdigit(),
                                 StateFilter(FSMTransmission.move_select_file))
    move_router.message.register(process_move_select_folder, Text(text=[lexicon['films'], lexicon['serials'],
                                                                        lexicon['another']]))
    move_router.message.register(process_final_move_torrent, Text(text=lexicon['yes']),
                                 StateFilter(FSMTransmission.move_accept))
    move_router.message.register(process_cancel_move_torrent, Text(text=lexicon['no']),
                                 StateFilter(FSMTransmission.move_accept))
    move_router.message.register(wrong_id_input,
                                 StateFilter(FSMTransmission.move_select_file, FSMTransmission.move_accept))
