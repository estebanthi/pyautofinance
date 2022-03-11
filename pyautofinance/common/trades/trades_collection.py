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
