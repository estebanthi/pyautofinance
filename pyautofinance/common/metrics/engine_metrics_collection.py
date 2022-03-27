from pyautofinance.common.engine.engine_component import EngineComponent
from pyautofinance.common.metrics.metrics_collection import MetricsCollection


class EngineMetricsCollection(EngineComponent, MetricsCollection):

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
