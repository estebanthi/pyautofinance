import backtrader as bt

from ccxtbt import CCXTStore

from pyautofinance.common.broker.BrokerConfig import BrokerConfig


class BrokersFactory:

    @staticmethod
    def get_broker(broker_options):
        broker = None

        if broker_options.exchange:  # Means we're looking for ccxt broker
            broker_config = BrokerConfig(broker_options)
            store = CCXTStore(exchange=broker_options.exchange.id, currency=broker_options.currency,
                              config=broker_config.get_live_config(), retries=5,
                              debug=False)
            broker = store.getbroker()

        if broker_options.cash:  # Means we're looking for a backtesting broker
            broker = bt.brokers.BackBroker()
            broker.set_cash(broker_options.cash)
            broker.setcommission(broker_options.commission/100)

        return broker
