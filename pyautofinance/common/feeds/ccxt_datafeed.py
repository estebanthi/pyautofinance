from pyautofinance.common.feeds.live_datafeed import LiveDatafeed
from pyautofinance.common.brokers import CCXTLiveBroker


class CCXTDatafeed(LiveDatafeed):

    def _get_datafeed(self):
        broker = CCXTLiveBroker(broker_options)
        store = broker.get_store()
        return store.getdata(dataname=formatted_symbol, name=formatted_symbol, timeframe=timeframe.bt_timeframe,
                             fromdate=start_date, compression=timeframe.bt_compression, ohlcv_limit=99999,
                             sessionstart=start_date)