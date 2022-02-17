from ccxt import bitfinex, binance
import datetime as dt
from models.CandlesExtractor.CandlesExtractor import CandlesExtractor
from utils.dates import epoch_to_datetime
import pandas as pd


class CCXTCandlesExtractor(CandlesExtractor):

    def extract_candles(self):
        exchange = binance() if "BNB" in self.feed_options.market_options.symbol else bitfinex()
        print(exchange)
        timestamp = int(dt.datetime.timestamp(self.feed_options.time_options.start_date) * 1000)
        limit_candles = exchange.fetch_ohlcv(
            symbol=self.format_symbol(),
            timeframe=self.format_timeframe(),
            since=timestamp,
            limit=10000
        )
        all_candles = self.bypass_candles_limit(limit_candles, exchange)
        formatted_candles = format_candles(all_candles)
        return formatted_candles

    def bypass_candles_limit(self, source_candles, exchange):
        while source_candles[-1][0] < dt.datetime.timestamp(
                self.feed_options.time_options.end_date) * 1000:  # If more than 10 000 candles

            candles_to_add = exchange.fetch_ohlcv(
                symbol=self.format_symbol(),
                timeframe=self.format_timeframe(),
                since=source_candles[-1][0],
                limit=10000
            )

            merge_candles(source_candles, candles_to_add)

        print(source_candles)
        return source_candles

    def format_symbol(self):
        return self.feed_options.market_options.symbol.replace("-", "/")

    def format_timeframe(self):
        return self.feed_options.time_options.timeframe.value[::-1]


def format_candles(candles, ):
    columns = 'Date Open High Low Close Volume'.split(
        ' ')

    formatted_candles = pd.DataFrame(candles, columns=columns)
    formatted_candles = formatted_candles.astype('float64')

    formatted_candles.loc[:, "Date"] = formatted_candles.loc[:, "Date"].apply(epoch_to_datetime)

    return formatted_candles


def merge_candles(source_candles, candles_to_add):
    for i in range(len(candles_to_add)):
        if i != 0:
            source_candles.append(candles_to_add[i])
