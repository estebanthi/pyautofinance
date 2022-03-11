from pyautofinance.common.analyzers.analyzer import Analyzer
from pyautofinance.common.engine.engine_component import EngineComponent


class MetricsCollection(EngineComponent):

    def __init__(self, metrics_list):
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
        for metric in self._metrics_list:
            bt_analyzer = metric.bt_analyzer
            analyzer_name = metric.analyzer_name
            analyzer = Analyzer(bt_analyzer, analyzer_name)
            analyzer.attach_to_engine(engine)
