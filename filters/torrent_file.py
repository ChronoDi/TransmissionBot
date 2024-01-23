from aiogram.types import Message
from aiogram.filters import BaseFilter


class IsTorrent(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.content_type == 'document' and message.document.file_name.endswith('.torrent')


class IsTorrentUrl(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.content_type == 'text' and message.text.startswith('magnet')
