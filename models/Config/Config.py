from models.Config.ConfigLoader import ConfigLoader
from models.Exceptions.ConfigFieldMissing import ConfigFieldMissing


class Config:

    def __init__(self):
        config_loader = ConfigLoader("config.yml")
        self.config = config_loader.get_config()

    def get_field(self, field):
        field_value = self.config.get(field)
        if not field_value:
            raise ConfigFieldMissing(field)
        return field_value

    def get_datasets_pathname(self):
        return self.get_field("datasets_pathname")
