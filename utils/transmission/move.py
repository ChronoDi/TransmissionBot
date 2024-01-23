
from utils.transmission import client
from config_data import config


def move_torrent(torrent_id: int, path: str) -> None:
    download_dir: str = f'{config.transmission.download_folder}{path}'
    client.move_torrent_data(torrent_id, location=download_dir)
