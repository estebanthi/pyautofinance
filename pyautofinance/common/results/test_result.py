from pyautofinance.common.metrics.metrics_collection import MetricsCollection


class TestResult:

    def __init__(self, *metrics):
        self.metrics = MetricsCollection(*metrics)

    def __getitem__(self, item):
        return self.metrics[item]
    