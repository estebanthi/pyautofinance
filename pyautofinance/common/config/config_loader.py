from yaml import safe_load

from pyautofinance.common.exceptions.config import ConfigFileNotFound


class ConfigLoader:

    def __init__(self, path_to_config):
        try:
            with open(path_to_config, 'r') as config_file:
                self._config = safe_load(config_file)
        except IOError:
            raise ConfigFileNotFound

    def get_config(self):
        return self._config
