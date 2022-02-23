import unittest

from pyautofinance.common.TelegramBot import TelegramBot


class TestTimeOptions(unittest.TestCase):

    def test_send_message(self):
        bot = TelegramBot()
        bot.send_message('Test')


if __name__ == '__main__':
    unittest.main()
