from transmission_rpc import Torrent

from utils.transmission import client


def delete_torrent(torrent_id: int) -> None:
    client.remove_torrent(ids=torrent_id, delete_data=True)
