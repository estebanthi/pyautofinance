from pyautofinance.common.engine.engine_component import EngineComponent


class EngineMetricsCollection(EngineComponent):

    def __init__(self, *metrics_list):
        self._metrics_list = metrics_list

    def __getitem__(self, item):
        for metric in self._metrics_list:
            if metric.name == item:
                return metric

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._metrics_list):
            metric = self._metrics_list[self._index]
            self._index += 1
            return metric
        else:
            raise StopIteration

    def __repr__(self):
        metrics_list = []
        for metric in self._metrics_list:
            metrics_list.append(str(metric))
        return ' '.join(metrics_list)

    def __list__(self):
        return self._metrics_list

    def attach_to_engine(self, engine):
        analyzers = self._get_analyzers()
        for analyzer in analyzers:
            analyzer.attach_to_engine(engine)

    def _get_analyzers(self):
        analyzers = []
        for metric in self._metrics_list:
            analyzers.append(metric.analyzer)
        nodups = self._remove_duplicates_analyzers(analyzers)
        return nodups

    @staticmethod
    def _remove_duplicates_analyzers(analyzers):
        nodups = []
        for analyzer in analyzers:
            if analyzer not in nodups:
                nodups.append(analyzer)
        return nodups

    def get_strat_metrics(self, strat):
        metrics = {}
        for metric in self._metrics_list:
            metrics[metric.name] = metric(strat)
        return metrics
