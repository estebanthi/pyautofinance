from telegram.ext import Updater

from pyautofinance.common.config.config import Config


class TelegramBot:

    def __init__(self):
        config = Config()
        token = config['telegram_token']
        self.user = config['user']
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def send_message(self, message):
        self.updater.bot.sendMessage(chat_id=self.user, text=message)

    def send_file(self, file):
        self.updater.bot.sendDocument(chat_id=self.user, document=file)
