from aiogram import Router, Bot
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from transmission_rpc import TransmissionError

from config_data import config
from lexicon import lexicon
from keyboards.fabric import get_reply_keyboard
from services.logs import logging
from states.transmission import FSMTransmission
from services.process_folder import get_name
from filters.torrent_file import IsTorrent, IsTorrentUrl
from utils.transmission.download import download_by_link, download_by_file


download_router: Router = Router()


async def process_download_message(message: Message, state: FSMContext):
    await message.answer(text=lexicon['select_folder'],
                         reply_markup=get_reply_keyboard(names=[lexicon['films'],
                                                                lexicon['serials'],
                                                                lexicon['another'],
                                                                lexicon['main_menu']], width=3))
    await state.set_state(FSMTransmission.download)


async def process_folder_message(message: Message, state: FSMContext):
    await state.update_data(folder=get_name(message.text))
    await message.answer(text=lexicon['take_url_file'],
                         reply_markup=get_reply_keyboard(names=[lexicon['main_menu']]))
    await state.set_state(FSMTransmission.take_url_file)


async def wrong_folder_message(message: Message):
    await message.answer(text=lexicon['wrong_folder'])


async def process_url(message: Message, state: FSMContext):
    state_data: dict[str:str | int] = await state.get_data()
    url = message.text
    path = state_data['folder']
    try:
        torrent = download_by_link(url=url, path=path)
        logging(f'File "{torrent.name}" download to folder {config.transmission.download_folder}{path} '
                f'by {message.from_user.username}')
        await state.clear()
        await message.answer(text=lexicon['correct_url'],
                             reply_markup=get_reply_keyboard(names=[lexicon['main_menu']]))
    except TransmissionError:
        await message.answer(text=lexicon['incorrect_url'])


async def wrong_url_file(message: Message):
    await message.answer(text=lexicon['incorrect_url'])


async def process_file(message: Message, bot: Bot,  state: FSMContext):
    state_data: dict[str:str | int] = await state.get_data()
    file = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file.file_path)
    path = state_data['folder']
    try:
        torrent = download_by_file(downloaded_file, state_data['folder'])
        logging(f'File "{torrent.name}" download to folder {config.transmission.download_folder}{path} '
                f'by {message.from_user.username}')
        await state.clear()
        await message.answer(text=lexicon['correct_file'],
                             reply_markup=get_reply_keyboard(names=[lexicon['main_menu']]))
    except TransmissionError:
        await message.answer(text=lexicon['incorrect_file'])


def process_all_handlers() -> None:
    download_router.message.register(process_download_message,
                                     Text(text=lexicon["download"]), StateFilter(FSMTransmission.menu))

    download_router.message.register(process_folder_message, Text(text=[lexicon['films'], lexicon['serials'],
                                                                        lexicon['another']]),
                                     StateFilter(FSMTransmission.download))

    download_router.message.register(wrong_folder_message, StateFilter(FSMTransmission.download))

    download_router.message.register(process_url, IsTorrentUrl(), StateFilter(FSMTransmission.take_url_file))

    download_router.message.register(process_file, IsTorrent(), StateFilter(FSMTransmission.take_url_file))

    download_router.message.register(wrong_url_file, StateFilter(FSMTransmission.take_url_file))
