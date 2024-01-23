from transmission_rpc import Torrent

from utils.transmission import client
from config_data import config


def download_by_link(url: str, path: str) -> Torrent:
    download_dir: str = f'{config.transmission.download_folder}{path}'
    return client.add_torrent(url, download_dir=download_dir)


def download_by_file(file, download_path: str) -> Torrent:
    download_dir: str = f'{config.transmission.download_folder}{download_path}'
    return client.add_torrent(file, download_dir=download_dir)
