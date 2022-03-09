from pyautofinance.common.engine.engine_cerebro import EngineCerebro


class Engine:

    def __init__(self, components_assembly):
        self._components_assembly = components_assembly
        self.cerebro = EngineCerebro()

    def _build(self):
        for component in self._components_assembly:
            component.attach_to_engine(self)

    def run(self):
        self.cerebro = EngineCerebro()
        self._build()

        cerebro_result = self.cerebro.run(optreturn=True, tradehistory=True, maxcpus=1)
        return Result(cerebro_result)

    def plot(self, scheme={"style": 'candlestick', "barup": "green"}):
        self.cerebro.plot(**scheme)
