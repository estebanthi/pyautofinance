import backtrader as bt
import datetime as dt
import numpy as np

from pyautofinance.common.engine.Engine import Engine
from pyautofinance.common.options import EngineOptions, MarketOptions, TimeOptions, FeedOptions, BrokerOptions,\
    Market, WritingOptions
from pyautofinance.common.strategies.StrategiesFactory import StrategiesFactory
from pyautofinance.common.strategies.usable_strategies.TestBracketStrategy import TestBracketStrategy
from pyautofinance.common.sizers.SizersFactory import SizersFactory
from pyautofinance.common.feeds.FeedTitle import FeedTitle
from pyautofinance.common.analyzers.AnalyzersFactory import AnalyzersFactory
from pyautofinance.common.analyzers.FullMetrics import FullMetrics
from pyautofinance.common.timeframes import d1
from pyautofinance.common.testers.SplitTrainTestTester import SplitTrainTestTester
from pyautofinance.common.metrics import TotalGrossProfit


market_options = MarketOptions(Market.CRYPTO, 'BTC-EUR')
time_options = TimeOptions(dt.datetime(2020, 1, 1), d1(), dt.datetime(2022, 1, 1))
feed_options = FeedOptions(market_options, time_options)

broker_options = BrokerOptions(100_000, 0.2)

strategy = StrategiesFactory().make_strategy(TestBracketStrategy, logging=False, stop_loss=np.linspace(1, 10, 3),
                                             risk_reward=np.linspace(1, 10, 3), period_me1=range(6, 18, 3),
                                             period_me2=range(22, 35, 3), period_signal=9)
sizer = SizersFactory().make_sizer(bt.sizers.PercentSizer, percents=10)

tradeanalyzer = AnalyzersFactory().make_analyzer(bt.analyzers.TradeAnalyzer)
fullmetrics = AnalyzersFactory().make_analyzer(FullMetrics, _name='full_metrics')

writing_options = WritingOptions(candles_destination=FeedTitle(feed_options).get_pathname())

engine_options = EngineOptions(broker_options, feed_options, [strategy], sizer, analyzers=[tradeanalyzer],
                               writing_options=writing_options, metrics=[TotalGrossProfit])

tester = SplitTrainTestTester()
test_result = tester.test(engine_options, TotalGrossProfit, 20)

print(test_result['BTC-EUR'][0].metrics['TotalGrossProfit'])
print(test_result['BTC-EUR'][0].params)
