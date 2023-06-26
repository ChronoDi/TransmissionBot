from aiogram import Router

from .main_menu import process_all_handlers, main_menu_router
from .download import process_all_handlers, download_router
from .look_files import process_all_handlers, look_files_router
from .delete import process_all_handlers, delete_router
from .move import process_all_handlers, move_router

from filters.admins import IsAdmin

router: Router = Router()
router.message.filter(IsAdmin())


def process_transmission_handlers():
    main_menu.process_all_handlers()
    download.process_all_handlers()
    look_files.process_all_handlers()
    delete.process_all_handlers()
    move.process_all_handlers()


def include_transmission_routers():
    router.include_router(main_menu_router)
    router.include_router(download_router)
    router.include_router(look_files_router)
    router.include_router(delete_router)
    router.include_router(move_router)


process_transmission_handlers()
include_transmission_routers()
