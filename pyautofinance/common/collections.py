class MetricsCollection:

    def __init__(self, metrics_list):
        self.metrics_list = metrics_list

    def __getitem__(self, item):
        for metric in self.metrics_list:
            if metric.name == item:
                return metric

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.metrics_list):
            metric = self.metrics_list[self.index]
            self.index += 1
            return metric
        else:
            raise StopIteration

    def __repr__(self):
        metrics_list = []
        for metric in self.metrics_list:
            metrics_list.append(str(metric))
        return ' '.join(metrics_list)


class ParamsCollection:

    def __init__(self, params_list):
        self.params_list = params_list

    def __getitem__(self, item):
        return self.params_list[item]

    def __iter__(self):
        for key, value in self.params_list:
            yield key, value

    def __repr__(self):
        params_list = []
        for param in self.params_list:
            params_list.append(str(param))
        return ' '.join(params_list)


class TradesCollection:

    def __init__(self, trades_list):
        self.trades_list = trades_list

    def __getitem__(self, item):
        return self.trades_list[item]

    def __iter__(self):
        for trade in self.trades_list:
            yield trade

    def __repr__(self):
        trades_list = []
        for trade in self.trades_list:
            trades_list.append(str(trade))
        return ' '.join(trades_list)


class StratsCollection:

    def __init__(self, strats_list):
        self.strats_list = strats_list

    def __getitem__(self, item):
        return self.strats_list[item]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.strats_list):
            strat = self.strats_list[self.index]
            self.index += 1
            return strat
        else:
            raise StopIteration

    def sort_by_metric(self, metric):
        metric_name = metric.name
        sorted_strats_list = sorted(self.strats_list, key=lambda strat: strat.metrics[metric_name], reverse=True)
        return StratsCollection(sorted_strats_list)

