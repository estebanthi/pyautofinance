from sklearn.metrics import f1_score

from pyautofinance.common.metrics.learn_metrics.learn_metric import LearnMetric


class F1Score(LearnMetric):

    name = 'F1Score'
    value = 0

    def _get_metric_value(self):
        return f1_score(self.y_true, self.y_pred)

    def __gt__(self, other):
        return self.value > other.value
