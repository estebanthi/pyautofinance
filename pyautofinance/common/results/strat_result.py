from pyautofinance.common.results.params_collection import ParamsCollection
from pyautofinance.common.trades.trades_collection import TradesCollection


class StratResult:

    def __init__(self, strat, metrics_collection):
        self._strat = strat
        self._metrics_collection = metrics_collection

        self.params = self._build_params_collection()
        self.trades = self._build_trades_collection()
        self.metrics = self._build_metrics()

    def _build_params_collection(self):
        params_list = self._get_params_from_strat(self._strat)
        return ParamsCollection(params_list)

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
        trade_list = self._strat.analyzers.tradelist.get_analysis()
        return TradesCollection(trade_list)

    def _build_metrics(self):
        return self._metrics_collection.get_strat_metrics(self._strat)

    def get_metric(self, metric):
        return self.metrics[metric]
