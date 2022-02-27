from pyautofinance.common.metrics import MetricsCollection
from pyautofinance.common.params import ParamsCollection


class Result:

    def __init__(self, engine_result, metrics_to_use):
        self.engine_result = engine_result
        self.metrics_to_use = metrics_to_use
        self.metrics = self.get_metrics()
        self.params = self.get_params()

    def __getitem__(self, item):
        metrics = self.metrics[item]
        params = self.params[item]
        return metrics, params

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.engine_result):
            symbol = list(self.engine_result.keys())[self.index]
            metrics = self.metrics[symbol]
            params = self.params[symbol]

            self.index += 1
            return symbol, metrics, params
        else:
            raise StopIteration


    def get_metrics(self):
        metrics = {}
        for symbol, result in self.engine_result.items():
            metrics_collections = []
            for strat in result:
                for optimized_strat in strat:
                    metrics_list = []
                    if self.metrics_to_use:
                        for metric in self.metrics_to_use:
                            metrics_list.append(metric(optimized_strat))
                        metrics_collection = MetricsCollection(metrics_list)
                        metrics_collections.append(metrics_collection)
            metrics[symbol] = metrics_collections
        return metrics

    def get_params(self):
        params = {}
        for symbol, result in self.engine_result.items():
            params_collections = []
            for strat in result:
                for optimized_strat in strat:
                    params_list = self._get_params_from_strat(optimized_strat)
                    params_collections.append(ParamsCollection(params_list))
            params[symbol] = params_collections
        return params

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

