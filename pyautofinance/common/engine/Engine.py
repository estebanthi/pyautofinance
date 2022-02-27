import backtrader as bt

from enum import Enum

from pyautofinance.common.broker.BrokersFactory import BrokersFactory
from pyautofinance.common.strategies.StrategiesFactory import StrategyType
from pyautofinance.common.feeds.extractors import CandlesExtractorsFactory
from pyautofinance.common.feeds.datafeeds_generators import DatafeedGeneratorsFactory
from pyautofinance.common.feeds.writers import CandlesWriter
from pyautofinance.common.options import WritingOptions
from pyautofinance.common.engine.EngineCerebro import EngineCerebro
from pyautofinance.common.engine.Result import Result
from pyautofinance.common.analyzers.AnalyzersFactory import AnalyzersFactory


class RunningMode(Enum):
    SIMPLE = 'SIMPLE'
    OPTIMIZED = 'OPTIMIZED'


class Engine:

    def __init__(self, engine_options):
        self.engine_options = engine_options
        self.cerebro = EngineCerebro()

    def multirun(self, symbols, candles_destinations=None):
        engine_options = self.engine_options

        results = self._multirun_and_write_candles(symbols, candles_destinations, engine_options)\
            if candles_destinations else self._multirun_without_writing_candles(symbols, engine_options)

        return Result(results, engine_options.metrics)

    def _multirun_and_write_candles(self, symbols, candles_destinations, engine_options):
        results = {}
        for symbol, candles_destination in zip(symbols, candles_destinations):
            engine_options.feed_options.market_options.symbol = symbol
            engine_options.writing_options = self._get_writing_options(engine_options, candles_destination)
            result = self._run(engine_options)
            results.update(result)
        return results

    @staticmethod
    def _get_writing_options(engine_options, candles_destination):
        results_destination = None

        if engine_options.writing_options:
            results_destination = engine_options.writing_options.results_destination

        if results_destination:
            return WritingOptions(candles_destination, results_destination)
        else:
            return WritingOptions(candles_destination)

    @staticmethod
    def _convert_results_list_into_dict(results_list):
        result = results_list[0]
        for res in results_list:
            result.update(res)
        return result

    def _multirun_without_writing_candles(self, symbols, engine_options):
        results = {}
        for symbol in symbols:
            engine_options.feed_options.market_options.symbol = symbol
            result = self._run(engine_options)
            results.update(result)
        return results

    def run(self):
        return Result(self._run(self.engine_options), self.engine_options.metrics)

    def _run(self, engine_options):
        cerebro = EngineCerebro()

        strategies = engine_options.strategies
        running_mode = self._choose_running_mode(strategies)
        self._add_strategies_to_cerebro(cerebro, strategies, running_mode)

        options_analyzers = engine_options.analyzers
        analyzers = self._get_analyzers_from_metrics(engine_options)
        if options_analyzers:
            analyzers = options_analyzers + analyzers
        self._add_analyzers_to_cerebro(cerebro, analyzers)

        observers = engine_options.observers
        self._add_observers_to_cerebro(cerebro, observers)

        sizer = engine_options.sizer
        self._add_sizer_to_cerebro(cerebro, sizer)

        timers = engine_options.timers
        self._add_timers_to_cerebro(cerebro, timers)

        self._add_writer_to_cerebro(cerebro, engine_options)

        broker = self._get_broker(engine_options)
        self._add_broker_to_cerebro(cerebro, broker)

        self._add_datafeed_to_cerebro_and_resample_if_needed(cerebro, engine_options)
        engine_result = cerebro.run(optreturn=True, tradehistory=True, maxcpus=1)
        self.cerebro = cerebro  # We need to update it for plotting

        formatted_result = self._format_result(engine_options, running_mode, engine_result)
        return formatted_result

    @staticmethod
    def _format_result(engine_options, running_mode, result):
        if running_mode == RunningMode.SIMPLE:
            return {engine_options.feed_options.market_options.symbol: [result]}
        return {engine_options.feed_options.market_options.symbol: result}

    def _choose_running_mode(self, strategies):
        return RunningMode.OPTIMIZED if self._optimized_strategy_found_in_strategies(strategies) \
            else RunningMode.SIMPLE

    @staticmethod
    def _optimized_strategy_found_in_strategies(strategies):
        for strategy in strategies:
            if strategy.type == StrategyType.OPTIMIZED:
                return True

    @staticmethod
    def _add_broker_to_cerebro(cerebro, broker):
        cerebro.setbroker(broker)

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
        cerebro.addstrategy(strategy.strategy, **strategy.parameters)

    @staticmethod
    def _add_optimized_strategy_to_cerebro(cerebro, strategy):
        cerebro.optstrategy(strategy.strategy, **strategy.parameters)

    def _add_datafeed_to_cerebro_and_resample_if_needed(self, cerebro, engine_options):
        datafeed = self._add_and_return_datafeed_to_cerebro(cerebro, engine_options)
        self._resample_datafeed_if_needed(cerebro, datafeed, engine_options)

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
        return timeframes

    @staticmethod
    def _resample_datafeed_from_timeframes(cerebro, datafeed, timeframes):
        for timeframe in timeframes:
            cerebro.resampledata(datafeed, timeframe=timeframe.bt_timeframe, compression=timeframe.bt_compression)

    def _get_analyzers_from_metrics(self, engine_options):
        analyzers = self._get_bt_analyzers_from_metrics(engine_options.metrics)
        analyzers = self._remove_same_elements_from_list(analyzers)
        analyzers = self._make_analyzers_from_bt_analyzers_list(analyzers)
        return analyzers

    @staticmethod
    def _get_bt_analyzers_from_metrics(metrics):
        analyzers = []
        if metrics:
            for metric in metrics:
                analyzers.append(metric.analyzer_to_get_metric_from)
        return analyzers

    @staticmethod
    def _make_analyzers_from_bt_analyzers_list(analyzers):
        factory = AnalyzersFactory()
        copy = analyzers.copy()
        for index, analyzer in enumerate(analyzers):
            copy[index] = factory.make_analyzer(analyzer)
        return copy

    @staticmethod
    def _remove_same_elements_from_list(container):
        return list(set(container))

    @staticmethod
    def _add_analyzers_to_cerebro(cerebro, analyzers):
        if analyzers:
            for analyzer in analyzers:
                cerebro.addanalyzer(analyzer.analyzer, **analyzer.parameters)

    @staticmethod
    def _add_observers_to_cerebro(cerebro, observers):
        if observers:
            for observer in observers:
                cerebro.addanalyzer(observer.observer, **observer.parameters)

    @staticmethod
    def _add_sizer_to_cerebro(cerebro, sizer):
        cerebro.addsizer(sizer.sizer, **sizer.parameters)

    @staticmethod
    def _add_timers_to_cerebro(cerebro, timers):
        if timers:
            for timer in timers:
                cerebro.add_timer(timername=timer.name, function=timer.get_function(), **timer.parameters)

    @staticmethod
    def _add_writer_to_cerebro(cerebro, engine_options):
        if engine_options.writing_options:
            results_destination = engine_options.writing_options.results_destination
            if results_destination:
                cerebro.addwriter(bt.WriterFile, out=results_destination)

    def plot(self, scheme={"style": 'candlestick', "barup": "green"}):
        self.cerebro.plot(**scheme)
