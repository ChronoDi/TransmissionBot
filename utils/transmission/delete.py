from transmission_rpc import Torrent

from utils.transmission import client


def delete_torrent(torrent_id_list: list[int]) -> None:
    client.remove_torrent(ids=torrent_id_list, delete_data=True)
