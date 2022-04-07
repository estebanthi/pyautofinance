from pyautofinance.common.feeds.datafeed import Datafeed
from pyautofinance.common.brokers import CCXTLiveBroker


class CCXTDatafeed(Datafeed):

    def __init__(self, symbol, start_date, timeframe, exchange, currency, sandbox_mode=False):
        super().__init__(symbol, start_date, timeframe)
        self.exchange = exchange
        self.sandbox_mode = sandbox_mode
        self.currency = currency
        self.bt_datafeed = self._get_bt_datafeed()

    def _get_bt_datafeed(self):
        broker = CCXTLiveBroker(self.exchange, self.currency, self.sandbox_mode)
        store = broker.get_store()
        formatted_symbol = self._format_symbol()
        return store.getdata(dataname=formatted_symbol, name=formatted_symbol, timeframe=self.timeframe.bt_timeframe,
                             fromdate=self.start_date, compression=self.timeframe.bt_compression, ohlcv_limit=99999,
                             sessionstart=self.start_date)

    def _format_symbol(self):
        return self.symbol.replace('-', '/')

