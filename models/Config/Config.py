from models.Config.ConfigLoader import ConfigLoader
from models.Exceptions.ConfigFieldMissing import ConfigFieldMissing


class Config:

    def __init__(self):
        config_loader = ConfigLoader("config.yml")
        self.config = config_loader.get_config()

    def get_datasets_pathname(self):
        datasets_path = self.config.get("datasets_pathname")
        if not datasets_path:
            raise ConfigFieldMissing("datasets_pathname")
        return datasets_path
