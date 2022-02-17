from yaml import safe_load
import sys
from utils.exceptions import config_file_not_found


class ConfigLoader:

    def __init__(self, path_to_config):

        try:
            config_file = open(path_to_config, 'r')
            self.config = safe_load(config_file)
        except IOError as e:
            config_file_not_found()

    def get_config(self):
        return self.config
