import unittest
from models.Config.ConfigLoader import ConfigLoader

class TestCandlesExtractor(unittest.TestCase):

    def test_config_file(self):
        config_loader = ConfigLoader("config.yml")


if __name__ == '__main__':
    unittest.main()
