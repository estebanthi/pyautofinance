from sklearn.metrics import accuracy_score

from pyautofinance.common.metrics.learn_metrics.learn_metric import LearnMetric


class Accuracy(LearnMetric):

    name = 'Accuracy'
    value = 0

    def _get_metric_value(self):
        return accuracy_score(self.y_true, self.y_pred)

    def __gt__(self, other):
        return self.value > other.value
