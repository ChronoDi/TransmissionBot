from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Text, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from transmission_rpc import Torrent

from keyboards.pagination import get_pagination_keyboard
from states.transmission import FSMTransmission
from utils.paginator import get_current_page_from_list
from utils.transmission.look_files import get_torrents_dict, show_result
from keyboards.fabric import get_reply_keyboard
from lexicon import lexicon

look_files_router: Router = Router()


async def process_look_file(message: Message, state: FSMContext):
    result_dict, num_pages = await get_torrents_dict()
    await state.update_data(result_dict=result_dict, num_pages=num_pages, current_page=0)
    await message.answer(text=lexicon['torrent_list'],
                         reply_markup=get_reply_keyboard(names=[lexicon['delete'],
                                                                lexicon['move'],
                                                                lexicon['main_menu']]))
    await message.answer(text=show_result(result_dict['0']),
                         reply_markup=get_pagination_keyboard())
    await state.set_state(FSMTransmission.look_files)


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


def process_all_handlers() -> None:
    look_files_router.message.register(process_look_file, Text(text=lexicon['look_files']),
                                       StateFilter(FSMTransmission.menu))
    look_files_router.callback_query.register(process_paginator_torrents,
                                              or_f(F.data == 'previous', F.data == 'next'),
                                              or_f(StateFilter(FSMTransmission.look_files),
                                                   StateFilter(FSMTransmission.delete_select_file)))
    look_files_router.message.register(wrong_id_input,
                                       StateFilter(FSMTransmission.menu))
