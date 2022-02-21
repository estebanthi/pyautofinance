import unittest

from pyautofinance.common.exceptions.config import ConfigFileNotFound, ConfigFieldMissing

from pyautofinance.common.config import Config


class TestConfig(unittest.TestCase):

    existing_config_filename = "config.yml"
    existing_field = "datasets_pathname"

    non_existing_config_filename = "foo.yml"
    non_existing_field = "foo"

    def test_config_file_not_found(self):
        with self.assertRaises(ConfigFileNotFound):
            config = Config(self.non_existing_config_filename)

    def test_config_file_found(self):
        config = Config(self.existing_config_filename)

    def test_config_field_found(self):
        config = Config()
        config.get_field(self.existing_field)

    def test_config_field_not_found(self):
        config = Config()
        with self.assertRaises(ConfigFieldMissing):
            field = config.get_field(self.non_existing_field)


if __name__ == '__main__':
    unittest.main()
