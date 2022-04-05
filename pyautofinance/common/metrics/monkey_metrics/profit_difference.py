from pyautofinance.common.metrics.metric import Metric


class ProfitDifference(Metric):
    name = 'ProfitDifference'

    def __init__(self, strat_profit, monkey_average_profit):
        self.strat_profit = strat_profit
        self.monkey_average_profit = monkey_average_profit
        super().__init__()

    def _get_metric_value(self):
        return self.strat_profit - self.monkey_average_profit

    def __gt__(self, other):
        return self.value > other.value
