from aiogram import Router
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from lexicon import lexicon
from keyboards.fabric import get_reply_keyboard
from states.transmission import FSMTransmission

main_menu_router: Router = Router()


async def process_main_menu_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=lexicon['start'], reply_markup=get_reply_keyboard(names=[lexicon['transmission']]))


async def process_transmission_message(message: Message, state: FSMContext):
    await message.answer(text=lexicon['start'],
                         reply_markup=get_reply_keyboard(names=[lexicon['download'],
                                                                lexicon['look_files'],
                                                                lexicon['main_menu']], width=2))
    await state.set_state(FSMTransmission.menu)


def process_all_handlers() -> None:
    main_menu_router.message.register(process_main_menu_message, Text(text=lexicon['main_menu']))

    main_menu_router.message.register(process_transmission_message,
                                      Text(text=lexicon['transmission']), StateFilter(default_state))
