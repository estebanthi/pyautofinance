import unittest

from pyautofinance.common.config.config import Config
from pyautofinance.common.exceptions import ConfigFileNotFound, ConfigFieldMissing


class TestConfig(unittest.TestCase):

    def test_initialization(self):
        config = Config()
        self.assertTrue(isinstance(config, Config))

    def test_suscription(self):
        config = Config()
        config['ohlcv_pathname']

    def test_config_not_found(self):
        with self.assertRaises(ConfigFileNotFound):
            config = Config('ofkeofk')

    def test_field_not_found(self):
        config = Config()
        with self.assertRaises(ConfigFieldMissing):
            config['ofkoe']


if __name__ == '__main__':
    unittest.main()
