from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admins: list[int]


@dataclass
class Redis:
    is_need: bool
    host: str


@dataclass
class Transmission:
    ip: str
    port: int
    user: str
    password: str
    download_folder: str
    film_folder: str
    serial_folder: str
    another_folder: str


@dataclass
class Config:
    tg_bot: TgBot
    redis: Redis
    transmission: Transmission


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admins=list(map(int, env.list('ADMINS')))),
                  redis=Redis(host=env('REDIS_HOST'),
                              is_need=env.bool('USE_REDIS')),
                  transmission=Transmission(ip=env('TRANSMISSION_IP'),
                                            port=env.int('TRANSMISSION_PORT'),
                                            user=env('TRANSMISSION_USER_NAME'),
                                            password=env('TRANSMISSION_PASSWORD'),
                                            film_folder=env('FILM_FOLDER'),
                                            serial_folder=env('SERIAL_FOLDER'),
                                            another_folder=env('ANOTHER_FOLDER'),
                                            download_folder=env('DOWNLOAD_FOLDER')))

