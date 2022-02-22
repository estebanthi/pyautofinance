import time

from pyautofinance.common.config import Config


class BrokerConfig:

    def __init__(self, broker_options):
        self.broker_options = broker_options

    def get_live_config(self):
        exchange = self.broker_options.exchange
        api_key = self._load_api_key(exchange)
        api_secret = self._load_api_secret(exchange)
        return {
            'apiKey': api_key,
            'secret': api_secret,
            'nonce': lambda: str(int(time.time() * 1000)),
            'enableRateLimit': True,
        }

    @staticmethod
    def _load_api_key(exchange):
        api_key_field_name = f"{exchange.id}_api_key"
        config = Config()
        return config.get_field(api_key_field_name)

    @staticmethod
    def _load_api_secret(exchange):
        api_secret_field_name = f"{exchange.id}_api_secret"
        config = Config()
        return config.get_field(api_secret_field_name)


