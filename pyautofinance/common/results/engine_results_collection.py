import numpy as np


class EngineResultsCollection:

    def __init__(self, *engine_results_list):
        self.engine_results = engine_results_list

    def __getitem__(self, item):
        return self.engine_results[item]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.engine_results):
            engine_result = self.engine_results[self.index]
            self.index += 1
            return engine_result

        raise StopIteration

    def get_average_metric(self, metric):
        values_global = []
        for engine_result in self.engine_results:
            values_per_engine_result = []
            for strat_result in engine_result:
                values_per_engine_result.append(strat_result[metric].value)

            values_global.append(values_per_engine_result)

        return list(np.array(values_global).mean(axis=0))