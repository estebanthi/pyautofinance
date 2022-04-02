from pyautofinance.common.metrics.metrics_collection import MetricsCollection


class TestResult:

    def __init__(self, *metrics, valid=False):
        self.valid = valid
        self.metrics = MetricsCollection(*metrics)

    def __getitem__(self, item):
        return self.metrics[item]

    def validate(self, metrics, validation_functions):
        if isinstance(metrics, list) and isinstance(validation_functions, list):
            for metric, validation_function in zip(metrics, validation_functions):
                metric_name = metric if isinstance(metric, str) else metric.name
                metric_value = self[metric_name].value

                valid = validation_function(metric_value)
                if valid is False:
                    self.valid = False
                    return False
        else:
            metric_name = metrics if isinstance(metrics, str) else metrics.name
            metric_value = self[metric_name].value
            valid = validation_functions(metric_value)

        self.valid = valid
        return valid
