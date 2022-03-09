import backtrader as bt

from pyautofinance.common.analyzers import CustomReturns
from pyautofinance.common.analyzers import ReturnsVolatility
from pyautofinance.common.analyzers import TradesAverageReturns
from pyautofinance.common.analyzers import CalmarRatio
from backtrader.analyzers import SharpeRatio_A
from backtrader.analyzers import TradeAnalyzer
from backtrader.analyzers import DrawDown


class MetricsPack(bt.Analyzer):

    def __init__(self):
        self.custom_returns = CustomReturns()
        self.returns_volatility = ReturnsVolatility()
        self.sharpe_ratio = SharpeRatio_A()
        self.trade_analyzer = TradeAnalyzer()
        self.drawdown = DrawDown()
        self.trades_average_returns = TradesAverageReturns()
        self.calmar_ratio = CalmarRatio()

    def get_analysis(self):
        annual_returns = self.custom_returns.get_analysis()["annual_returns"]

        returns_volatility = self.returns_volatility.get_analysis()["volatility"]

        sharpe_ratio = self.sharpe_ratio.get_analysis()["sharperatio"]
        calmar_ratio = self.calmar_ratio.get_analysis()["calmar_ratio"]

        trade_analysis = self.trade_analyzer.get_analysis()

        pnl_net_total = trade_analysis["pnl"]["net"]["total"]
        pnl_gross_total = trade_analysis["pnl"]["gross"]["total"]
        fees = pnl_gross_total - pnl_net_total

        open_trades_nb = trade_analysis.total.open
        close_trades_nb = trade_analysis.total.closed
        close_shorts_nb = trade_analysis.short.total
        close_longs_nb = trade_analysis.long.total

        average_returns = self.trades_average_returns.get_analysis()["average_returns"]
        average_returns_short = self.trades_average_returns.get_analysis()["average_returns_short"]
        average_returns_long = self.trades_average_returns.get_analysis()["average_returns_long"]

        winrate = trade_analysis.won.total / close_trades_nb

        len_in_market = trade_analysis.len.total
        average_trade_len = trade_analysis.len.average
        longest_trade_len = trade_analysis.len.max
        average_won_len = trade_analysis.len.won.average
        average_lost_len = trade_analysis.len.lost.average

        drawdown = self.drawdown.get_analysis()
        average_drawdown = drawdown["drawdown"]
        average_drawdown_length = drawdown["len"]
        max_drawdown = drawdown["max"]["drawdown"]
        max_drawdown_length = drawdown["max"]["len"]

        return {
            "Annual returns": annual_returns,
            "PNL net": pnl_net_total,
            "Fees": fees,
            "Winrate": winrate,
            "Total trades": close_trades_nb,
            "Total long": close_longs_nb,
            "Total short": close_shorts_nb,
            "Open trades": open_trades_nb,
            "Average return per trade": average_returns,
            "Average return per long": average_returns_long,
            "Average return per short": average_returns_short,
            "Time in market": len_in_market,
            "Average trade len": average_trade_len,
            "Max trade len": longest_trade_len,
            "Average won len": average_won_len,
            "Average lost len": average_lost_len,
            "Average drawdown": average_drawdown,
            "Average drawdown length": average_drawdown_length,
            "Max drawdown": max_drawdown,
            "Max drawdown length": max_drawdown_length,
            "Annualized Sharpe ratio": sharpe_ratio,
            "Calmar ratio": calmar_ratio,
            "Returns volatility": returns_volatility,
        }