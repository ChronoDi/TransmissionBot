from transmission_rpc import Torrent

from utils.transmission import client


def delete_torrent(torrent: Torrent) -> None:
    client.remove_torrent(ids=torrent.id, delete_data=True)
