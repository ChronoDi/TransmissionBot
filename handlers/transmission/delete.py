from typing import Any
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Text, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from transmission_rpc import Torrent

from keyboards.pagination import get_pagination_keyboard
from states.transmission import FSMTransmission
from utils.paginator import slice_list, get_current_page_from_list
from utils.transmission.look_files import get_torrents_id_list, get_torrents, show_result
from utils.transmission.delete import delete_torrent
from keyboards.fabric import get_reply_keyboard
from services.logs import logging
from lexicon import lexicon

delete_router: Router = Router()


async def process_delete_file(message: Message, state: FSMContext):
    await message.answer(text=lexicon['torrents_id_to_remove'],
                         reply_markup=get_reply_keyboard(names=[lexicon['main_menu']]))
    await state.set_state(FSMTransmission.delete_select_file)


async def process_take_id_torrent(message: Message, state: FSMContext):
    torrents_id_list: list[int] = get_torrents_id_list(message.text)

    if torrents_id_list:
        # await state.update_data(torrent_id=torrent.id,
        #                         torrent_name=torrent.name)
        torrents_list: list[Torrent] = get_torrents(torrents_id_list)
        result_dict, num_pages = await slice_list(torrents_list, 5)
        await state.update_data(result_dict=result_dict,
                                num_pages=num_pages,
                                current_page=0,
                                torrents_id_list=torrents_id_list)
        await message.answer(text=lexicon['torrent_delete_accept'],
                             reply_markup=get_reply_keyboard(names=[lexicon['yes'],
                                                                    lexicon['no'],
                                                                    lexicon['main_menu']]))
        await message.answer(text=show_result(result_dict['0']),
                             reply_markup=get_pagination_keyboard())
        await state.set_state(FSMTransmission.delete_accept)
    else:
        await message.answer(lexicon['torrent_not_found'],
                             reply_markup=get_reply_keyboard(names=[lexicon['main_menu']]))


async def process_paginator_torrents(callback: CallbackQuery, state: FSMContext):
    is_next = True if callback.data == 'next' else False
    torrents: list[Torrent] = await get_current_page_from_list(state, is_next)
    keyboard = get_pagination_keyboard()

    try:
        await callback.message.edit_text(text=show_result(torrents), reply_markup=keyboard)
    except TelegramBadRequest:
        await callback.answer()


async def wrong_id_input(message: Message):
    await message.answer(text=lexicon['torrent_wrong_input'])


async def process_final_delete_torrent(message: Message, state: FSMContext):
    temp_dict: dict[str: Any] = await state.get_data()
    torrent_id_list: list[int] = temp_dict['torrents_id_list']
    delete_torrent(torrent_id_list)
    logging(f'Files with ids "{torrent_id_list}" delete by {message.from_user.username}')
    await state.clear()
    await message.answer(text=lexicon['torrent_file_removed'],
                         reply_markup=get_reply_keyboard(names=[lexicon['main_menu']]))


async def process_cancel_delete_torrent(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=lexicon['torrent_cancel_delete'],
                         reply_markup=get_reply_keyboard(names=[lexicon['main_menu']]))


def process_all_handlers() -> None:
    delete_router.message.register(process_delete_file, Text(text=lexicon['delete']),
                                   StateFilter(FSMTransmission.look_files))
    delete_router.message.register(process_take_id_torrent,
                                   StateFilter(FSMTransmission.delete_select_file))
    delete_router.callback_query.register(process_paginator_torrents,
                                          or_f(F.data == 'previous', F.data == 'next'),
                                          (StateFilter(FSMTransmission.delete_accept)))
    delete_router.message.register(process_final_delete_torrent, Text(text=lexicon['yes']),
                                   StateFilter(FSMTransmission.delete_accept))
    delete_router.message.register(process_cancel_delete_torrent, Text(text=lexicon['no']),
                                   StateFilter(FSMTransmission.delete_accept))
    delete_router.message.register(wrong_id_input,
                                   StateFilter(FSMTransmission.delete_select_file, FSMTransmission.delete_accept))
