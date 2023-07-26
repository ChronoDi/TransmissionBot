from transmission_rpc import Torrent

from utils.transmission import client
from lexicon import lexicon


def get_torrents_list() -> str:
    torrents = client.get_torrents()
    torrents.sort(key=lambda x: x.id, reverse=False)
    result = ''

    for torrent in torrents:
        result += lexicon['torrent_view'].format(id=torrent.id,
                                                 name=torrent.name,
                                                 available=torrent.percent_complete * 100,
                                                 dir=torrent.download_dir)

    return result


def try_get_torrent(value: int) -> Torrent | None:
    torrents = client.get_torrents()

    for torrent in torrents:
        if torrent.id == value:
            return torrent

    return
