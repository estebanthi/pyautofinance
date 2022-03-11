from pyautofinance.common.feeds.datafeed import Datafeed
from pyautofinance.common.brokers import CCXTLiveBroker


class CCXTDatafeed(Datafeed):

    def __init__(self, symbol, start_date, timeframe, exchange, currency):
        super().__init__(symbol, start_date, timeframe)
        self._exchange = exchange
        self._currency = currency
        self._bt_datafeed = self._get_datafeed()

    def _get_datafeed(self):
        broker = CCXTLiveBroker(self._exchange, self._currency)
        store = broker.get_store()
        formatted_symbol = self._format_symbol()
        return store.getdata(dataname=formatted_symbol, name=formatted_symbol, timeframe=self._timeframe.bt_timeframe,
                             fromdate=self._start_date, compression=self._timeframe.bt_compression, ohlcv_limit=99999,
                             sessionstart=self._start_date)

    def _format_symbol(self):
        return self._symbol.replace('-', '/')

