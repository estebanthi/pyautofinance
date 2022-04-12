from pyautofinance.common.results.params_collection import ParamsCollection
from pyautofinance.common.trades.trades_collection import TradesCollection
from pyautofinance.common.trades.trade import Trade


class StratResult:

    def __init__(self, strat, metrics_collection, datafeed):
        self._strat = strat
        self._metrics_collection = metrics_collection
        self.datafeed = datafeed

        self.params = self._build_params_collection()
        self.trades = self._build_trades_collection()
        self.metrics = self._build_metrics()

    def _build_params_collection(self):
        params_list = self._get_params_from_strat(self._strat)
        return ParamsCollection(*params_list)

    def _get_params_from_strat(self, strat):
        params_dict = dict(strat.params._getkwargs())
        params_list = self._convert_params_dict_into_params_list(params_dict)
        return params_list

    @staticmethod
    def _convert_params_dict_into_params_list(params_dict):
        params_list = []
        for param, value in params_dict.items():
            params_list.append((param, value))
        return params_list

    def _build_trades_collection(self):
        trade_list = self._strat.analyzers.trade_list.get_analysis()['trades']
        trade_list = [[value for value in trade.values()] for trade in trade_list]
        trade_list = [Trade(*trade) for trade in trade_list]
        return TradesCollection(trade_list)

    def _build_metrics(self):
        return self._metrics_collection.get_strat_metrics(self._strat)

    def __getitem__(self, item):
        return self.metrics[item]
