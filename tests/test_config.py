import unittest
from config.ConfigLoader import ConfigLoader
from exceptions.config.ConfigFileNotFound import ConfigFileNotFound
from exceptions.config.ConfigFieldMissing import ConfigFieldMissing
from config.Config import Config


class TestConfig(unittest.TestCase):

    existing_config_filename = "config.yml"
    existing_field = "datasets_pathname"

    non_existing_config_filename = "foo.yml"
    non_existing_field = "foo"

    def test_config_file_not_found(self):
        with self.assertRaises(ConfigFileNotFound):
            config_loader = ConfigLoader(self.non_existing_config_filename)

    def test_config_file_found(self):
        config_loader = ConfigLoader(self.existing_config_filename)

    def test_config_field_found(self):
        config = Config()
        config.get_field(self.existing_field)

    def test_config_field_not_found(self):
        config = Config()
        with self.assertRaises(ConfigFieldMissing):
            field = config.get_field(self.non_existing_field)


if __name__ == '__main__':
    unittest.main()
