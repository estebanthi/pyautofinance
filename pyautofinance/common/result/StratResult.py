from pyautofinance.common.collections import MetricsCollection, ParamsCollection


class StratResult:

    def __init__(self, strat, metrics_to_use):
        self._strat = strat
        self._metrics_to_use = metrics_to_use

        self.metrics = self._build_metrics_collection()
        self.params = self._build_params_collection()

    def _build_metrics_collection(self):
        metrics_list = []
        if self._metrics_to_use:
            for metric in self._metrics_to_use:
                metrics_list.append(metric(self._strat))
        return MetricsCollection(metrics_list)

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