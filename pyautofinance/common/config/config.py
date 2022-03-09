from pyautofinance.common.exceptions.config import ConfigFieldMissing
from pyautofinance.common.config.config_loader import ConfigLoader


class Config:

    def __init__(self, config_filename="config.yml"):
        config_loader = ConfigLoader(config_filename)
        self._config = config_loader.get_config()

    def __getitem__(self, item):
        field_value = self._config.get(item)
        if not field_value:
            raise ConfigFieldMissing(item)
        return field_value
