from lexicon import lexicon
from config_data import config


def get_name(text: str) -> str:
    if text == lexicon['films']:
        return config.transmission.film_folder

    if text == lexicon['serials']:
        return config.transmission.serial_folder

    return config.transmission.another_folder
