from abc import abstractmethod

import backtrader as bt

from pyautofinance.common.engine.engine_component import EngineComponent


class Analyzer(EngineComponent):

    @abstractmethod
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_bt_analyzer(self) -> bt.Analyzer:
        pass

    def get_parameters(self):
        return {}

    def attach_to_engine(self, engine):
        engine.cerebro.addanalyzer(self.get_bt_analyzer(), _name=self.name, **self.get_parameters())

    def __eq__(self, other):
        return self.get_bt_analyzer() == other.get_bt_analyzer() and self.get_parameters() == other.get_parameters()
