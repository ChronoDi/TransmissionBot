from transmission_rpc import Torrent

from utils.paginator import slice_list
from utils.transmission import client
from lexicon import lexicon


async def get_torrents_dict() -> tuple[dict[str, list], int]:
    torrents: list[Torrent] = client.get_torrents()
    torrents.sort(key=lambda x: x.id, reverse=False)

    result_dict, num_pages = await slice_list(torrents, 5)

    return result_dict, num_pages


def show_result(torrents: list[Torrent]) -> str:
    result = ''

    for torrent in torrents:
        result += lexicon['torrent_view'].format(id=torrent.id,
                                                 name=torrent.name,
                                                 available=torrent.percent_complete * 100,
                                                 dir=torrent.download_dir)

    return result


def get_torrents(ids: list[int]) -> list[Torrent]:
    return client.get_torrents(ids)


def get_torrents_id_list(user_input: str) -> list[int]:
    str_torrents_list: list[str] = user_input.split(',')
    torrents_list: list[int] = []

    for value in str_torrents_list:
        try:
            temp = int(value)
            if try_get_torrent(temp):
                torrents_list.append(temp)
        except ValueError:
            continue

    return torrents_list


def try_get_torrent(value: int) -> bool:
    torrents = client.get_torrents()

    for torrent in torrents:
        if torrent.id == value:
            return True

    return False
