import backtrader as bt
from pyautofinance.common.trades import Trade
from pyautofinance.common.trades import TradeSide


class TradeList(bt.Analyzer):

    def get_analysis(self):
        return self.trades

    def __init__(self):
        self.trades = []

    def notify_trade(self, trade):

        if trade.isclosed:

            brokervalue = self.strategy.broker.getvalue()

            side = TradeSide.SHORT
            if trade.history[0].event.size > 0: side = TradeSide.LONG

            pricein = trade.history[len(trade.history) - 1].status.price
            priceout = trade.history[len(trade.history) - 1].event.price
            datein = bt.num2date(trade.history[0].status.dt)
            dateout = bt.num2date(trade.history[len(trade.history) - 1].status.dt)
            if trade.data._timeframe >= bt.TimeFrame.Days:
                datein = datein.date()
                dateout = dateout.date()

            pcntchange = 100 * priceout / pricein - 100
            pnl = trade.history[len(trade.history) - 1].status.pnlcomm
            pnlpcnt = 100 * pnl / brokervalue
            barlen = trade.history[len(trade.history) - 1].status.barlen
            if barlen != 0:
                pbar = pnl / barlen
            else:
                pbar = 0

            size = value = 0.0
            for record in trade.history:
                if abs(size) < abs(record.status.size):
                    size = record.status.size
                    value = record.status.value

            highest_in_trade = max(trade.data.high.get(ago=0, size=barlen + 1))
            lowest_in_trade = min(trade.data.low.get(ago=0, size=barlen + 1))
            hp = 100 * (highest_in_trade - pricein) / pricein
            lp = 100 * (lowest_in_trade - pricein) / pricein
            if side == TradeSide.LONG:
                mfe = hp
                mae = lp
            if side == TradeSide.SHORT:
                mfe = -lp
                mae = -hp

            ref = trade.ref
            symbol = trade.data._name
            change_percent = round(pcntchange, 2)
            pnl_percent = round(pnlpcnt, 2)
            pnl_per_bar = round(pbar, 2)
            mfe_percent = round(mfe, 2)
            mae_percent = round(mae, 2)
            trade = Trade(ref, symbol, side, datein, pricein, dateout, priceout, change_percent, pnl, pnl_percent,
                          size, value, barlen, pnl_per_bar, mfe_percent, mae_percent)
            self.trades.append(trade)

