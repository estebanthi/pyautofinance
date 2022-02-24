import unittest

from pyautofinance.common.TelegramBot import TelegramBot
from pyautofinance.common.strategies.strat_loggers import TelegramLogger
from pyautofinance.common.options import *
from pyautofinance.common.strategies.StrategiesFactory import StrategiesFactory
from pyautofinance.common.strategies.usable_strategies.TestBracketStrategy import TestBracketStrategy
from pyautofinance.common.sizers.SizersFactory import SizersFactory
from pyautofinance.common.engine.Engine import Engine


class TestTelegramLogger(unittest.TestCase):

    def test_send_message(self):
        bot = TelegramBot()
        bot.send_message('Test')

    def test_telegram_logger(self):
        broker_options = BrokerOptions(100_000, 0.2)

        market_options = MarketOptions(Market.CRYPTO, 'BTC-EUR')
        time_options = TimeOptions(dt.datetime(2020, 1, 1), TimeFrame.h1, dt.datetime(2021, 6, 1))
        feed_options = FeedOptions(market_options, time_options)

        bot = TelegramBot()
        logging_options = LoggingOptions(every_iter=False)
        logger = TelegramLogger(bot, logging_options)
        strategies = [StrategiesFactory().make_strategy(TestBracketStrategy, [], logger=logger,
                                                        logging=True, stop_loss=2,
                                                        risk_reward=2)]

        sizer = SizersFactory().make_sizer(bt.sizers.PercentSizer, percents=20)

        engine_options = EngineOptions(broker_options, feed_options, strategies, sizer)

        engine = Engine(engine_options)
        result = engine.run()


if __name__ == '__main__':
    unittest.main()
