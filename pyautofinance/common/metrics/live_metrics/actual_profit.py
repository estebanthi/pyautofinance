from pyautofinance.common.metrics.live_metrics.live_metric import LiveMetric


class ActualProfit(LiveMetric):

    name = 'ActualProfit'

    def _get_value_from_strat(self, strat):
        return strat.initial_cash - strat.broker.cash

    def __gt__(self, other):
        return self.value > other.value
