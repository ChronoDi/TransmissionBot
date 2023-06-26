from transmission_rpc import Torrent

from utils.transmission import client
from config_data import config


def move_torrent(torrent: Torrent, path: str) -> None:
    download_dir: str = f'{config.transmission.download_folder}{path}'
    client.move_torrent_data(torrent.id, location=download_dir)
