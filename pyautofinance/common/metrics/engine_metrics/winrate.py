from pyautofinance.common.metrics.engine_metrics.engine_metric import EngineMetric
from pyautofinance.common.analyzers import TradeAnalyzer


class Winrate(EngineMetric):

    name = 'Winrate'
    analyzers = [TradeAnalyzer()]

    def _get_metric_from_analysis(self, analysis):
        return analysis[0].won.total/analysis.total.total

    def __gt__(self, other):
        return self.value > other.value
