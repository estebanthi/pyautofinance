import time

from ccxtbt import CCXTStore

from pyautofinance.common.config.config import Config
from pyautofinance.common.brokers.broker import Broker


class CCXTLiveBroker(Broker):

    def __init__(self, exchange, currency, sandbox_mode=False):
        self._exchange = exchange
        self._sandbox_mode = sandbox_mode
        self._currency = currency
        store = self.get_store()
        self._bt_broker = store.getbroker()

    def get_store(self):
        return CCXTStore(exchange=self._exchange.id, currency=self._currency, config=self._get_live_config(), retries=5,
                         debug=False, sandbox=self._sandbox_mode)

    def _configure(self):
        pass

    def _get_live_config(self):
        api_key = self._load_api_key(self._exchange)
        api_secret = self._load_api_secret(self._exchange)
        return {
            'apiKey': api_key,
            'secret': api_secret,
            'nonce': lambda: str(int(time.time() * 1000)),
            'enableRateLimit': True,
        }

    def _load_api_key(self, exchange):
        api_key_field_name = f"test_{exchange.id}_api_key" if self._sandbox_mode else f"{exchange.id}_api_key"
        config = Config()
        return config[api_key_field_name]

    def _load_api_secret(self, exchange):
        api_secret_field_name = f"test_{exchange.id}_api_secret" if self._sandbox_mode else f"{exchange.id}_api_secret"
        config = Config()
        return config[api_secret_field_name]
