from transmission_rpc import Client

from config_data import config

client: Client = Client(host=config.transmission.ip, port=config.transmission.port,
                        username=config.transmission.user, password=config.transmission.password)
