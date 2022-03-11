from pyautofinance.common.results.strat_result import StratResult


class EngineResult:

    def __init__(self, engine_result, metrics_collection):
        self._engine_result = engine_result
        self._metrics_collection = metrics_collection
        self._strats_results = self._get_strat_results()

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._strats_results):
            strat_result = self._strats_results[self._index]
            self._index += 1
            return strat_result
        raise StopIteration

    def __contains__(self, item):
        if item in self._engine_result:
            return True
        return False

    def __getitem__(self, item):
        return self._strats_results[item]

    def _get_strat_results(self):
        strats_results = []
        for strat in self._engine_result:
            strats_results.append(StratResult(strat[0], self._metrics_collection))
        return strats_results

    def sort_by_metric(self, metric):
        sorted_results = sorted(self._strats_results,
                                key=lambda strat_result: strat_result.get_metric(metric), reverse=True)
        return sorted_results

    def get_best_params(self, metric):
        return self.sort_by_metric(metric)[0].params

