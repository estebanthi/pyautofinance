from abc import abstractmethod
from pyautofinance.common.engine.engine_component import EngineComponent


class Timer(EngineComponent):

    def __init__(self, when, **parameters):
        self.when = when
        self.parameters = parameters

    @abstractmethod
    def execute(self, cerebro, strat=None):  # Returns the function of the timer
        pass

    def attach_to_engine(self, engine):
        engine.cerebro.add_timer(self.when, execute=self.execute, **self.parameters)
