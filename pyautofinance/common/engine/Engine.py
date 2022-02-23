import backtrader as bt

from enum import Enum

from pyautofinance.common.broker.BrokersFactory import BrokersFactory
from pyautofinance.common.strategies.StrategiesFactory import StrategyType
from pyautofinance.common.feeds.extractors import CandlesExtractorsFactory
from pyautofinance.common.feeds.datafeeds_generators import DatafeedGeneratorsFactory
from pyautofinance.common.feeds.writers import CandlesWriter
from pyautofinance.common.options import TimeFrame


class RunningMode(Enum):
    SIMPLE = 'SIMPLE'
    OPTIMIZED = 'OPTIMIZED'


class Engine:

    def __init__(self, engine_options):
        self.engine_options = engine_options

    def run(self):
        cerebro = bt.Cerebro()

        strategies = self.engine_options.strategies
        running_mode = self._choose_running_mode(strategies)

        broker = self._get_broker(self.engine_options)
        cerebro.setbroker(broker)

        self._add_strategies_to_cerebro(cerebro, strategies, running_mode)

        datafeed = self._add_and_return_datafeed_to_cerebro(cerebro, self.engine_options)
        self._resample_datafeed_if_needed(cerebro, datafeed, self.engine_options)

        result = cerebro.run(optreturn=True, tradehistory=True)
        return result

    def _choose_running_mode(self, strategies):
        return RunningMode.OPTIMIZED if self._optimized_strategy_found_in_strategies(strategies) \
            else RunningMode.SIMPLE

    @staticmethod
    def _optimized_strategy_found_in_strategies(strategies):
        for strategy in strategies:
            if strategy.type == StrategyType.OPTIMIZED:
                return True

    @staticmethod
    def _get_broker(engine_options):
        factory = BrokersFactory()
        broker = factory.get_broker(engine_options.broker_options)
        return broker

    def _add_strategies_to_cerebro(self, cerebro, strategies, running_mode):
        if running_mode == RunningMode.SIMPLE:
            for strategy in strategies:
                self._add_simple_strategy_to_cerebro(cerebro, strategy)
        if running_mode == RunningMode.OPTIMIZED:
            for strategy in strategies:
                self._add_optimized_strategy_to_cerebro(cerebro, strategy)

    @staticmethod
    def _add_simple_strategy_to_cerebro(cerebro, strategy):
        cerebro.addstrategy(strategy.classname, **strategy.parameters)

    @staticmethod
    def _add_optimized_strategy_to_cerebro(cerebro, strategy):
        cerebro.optstrategy(strategy.classname, **strategy.parameters)

    def _add_and_return_datafeed_to_cerebro(self, cerebro, engine_options):
        candles = self._get_candles(engine_options)
        self._write_candles_if_requested(candles, engine_options)
        datafeed = self._get_datafeed(candles, engine_options)
        cerebro.adddata(datafeed)
        return datafeed

    @staticmethod
    def _get_candles(engine_options):
        feed_options = engine_options.feed_options
        candles = CandlesExtractorsFactory.get_candles(feed_options)
        return candles

    @staticmethod
    def _write_candles_if_requested(candles, engine_options):
        if engine_options.writing_options and engine_options.feed_options.time_options.end_date:
            if engine_options.writing_options.candles_destination:
                writer = CandlesWriter()
                writer.write(candles, engine_options.writing_options.candles_destination)

    @staticmethod
    def _get_datafeed(candles, engine_options):
        feed_options = engine_options.feed_options
        broker_options = engine_options.broker_options

        datafeed = DatafeedGeneratorsFactory.generate_datafeed(candles, feed_options, broker_options)
        return datafeed

    def _resample_datafeed_if_needed(self, cerebro, datafeed, engine_options):
        timeframes = self._collect_timeframes_from_strategies(engine_options.strategies)
        self._resample_datafeed_from_timeframes(cerebro, datafeed, timeframes)

    @staticmethod
    def _collect_timeframes_from_strategies(strategies):
        timeframes = []
        for strategy in strategies:
            if strategy.timeframes:
                for timeframe in strategy.timeframes:
                    timeframes.append(timeframe)
        return set(timeframes)

    @staticmethod
    def _resample_datafeed_from_timeframes(cerebro, datafeed, timeframes):
        for timeframe in timeframes:
            bt_timeframe, bt_compression = TimeFrame.get_bt_timeframe_and_compression_from_timeframe(timeframe)
            cerebro.resampledata(datafeed, timeframe=bt_timeframe, compression=bt_compression)