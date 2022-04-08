from pyautofinance.common.metrics.live_metrics.live_metric import LiveMetric


class LiveMetricsCollection():

    def __init__(self, *metrics_list):
        self._metrics_list = [metric() for metric in metrics_list]

    def update(self, strat):
        for metric in self._metrics_list:
            metric.update(strat)
