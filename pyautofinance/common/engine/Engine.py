import backtrader as bt

from pyautofinance.common.broker.BrokersFactory import BrokersFactory


class Engine:

    def run(self, engine_options):
        cerebro = bt.Cerebro()
        broker = self.get_broker(engine_options)
        cerebro.setbroker(broker)

    @staticmethod
    def configure_broker(engine_options):
        factory = BrokersFactory()
        broker = factory.get_broker(engine_options.broker_options)
        return broker
