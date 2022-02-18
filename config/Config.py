from config.ConfigLoader import ConfigLoader
from exceptions.config.ConfigFieldMissing import ConfigFieldMissing


class Config:

    def __init__(self):
        config_loader = ConfigLoader("config.yml")
        self._config = config_loader.get_config()

    def get_field(self, field):
        field_value = self._config.get(field)
        if not field_value:
            raise ConfigFieldMissing(field)
        return field_value

    def get_datasets_pathname(self):
        return self.get_field("datasets_pathname")
