from sklearn.metrics import recall_score

from pyautofinance.common.metrics.learn_metrics.learn_metric import LearnMetric


class Recall(LearnMetric):

    name = 'Recall'
    value = 0

    def _get_metric_value(self):
        return recall_score(self.y_true, self.y_pred)

    def __gt__(self, other):
        return self.value > other.value
