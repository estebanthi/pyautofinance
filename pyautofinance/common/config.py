from yaml import safe_load

from pyautofinance.common.exceptions.config import ConfigFileNotFound, ConfigFieldMissing


class _ConfigLoader:

    def __init__(self, path_to_config):
        try:
            with open(path_to_config, 'r') as config_file:
                self._config = safe_load(config_file)
        except IOError as e:
            raise ConfigFileNotFound

    def get_config(self):
        return self._config


class Config:

    def __init__(self, config_filename="config.yml"):
        config_loader = _ConfigLoader(config_filename)
        self._config = config_loader.get_config()

    def get_field(self, field):
        field_value = self._config.get(field)
        if not field_value:
            raise ConfigFieldMissing(field)
        return field_value

    def get_datasets_pathname(self):
        return self.get_field("datasets_pathname")
