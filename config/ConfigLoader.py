from yaml import safe_load
from exceptions.config.ConfigFileNotFound import ConfigFileNotFound


class ConfigLoader:

    def __init__(self, path_to_config):
        try:
            config_file = open(path_to_config, 'r')
            self._config = safe_load(config_file)
        except IOError as e:
            raise ConfigFileNotFound

    def get_config(self):
        return self._config
