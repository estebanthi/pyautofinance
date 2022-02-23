from termcolor import colored
from tabulate import tabulate


class ResultsAnalyzer:

    def __init__(self, results):
        self.results = results

    def get_top_3_pnls_per_symbol(self):  # TradeAnalyzer is needed

        pnls = {}

        for symbol, result in self.results.items():

            if type(result[0]) is not list:
                pnls[symbol] = dict(result[0].analyzers.tradeanalyzer.get_analysis()['pnl']['net'])

            else:
                pnls_dict = {}
                for res in result:  # For loop for iterating in all strats
                    for strat in res:
                        analysis = strat.analyzers.tradeanalyzer.get_analysis()
                        pnl_dict = {  # Default dict if no PNL
                            "total": 0,
                            "average": 0,
                        }
                        if "pnl" in analysis:
                            pnl_dict = {
                                "total": strat.analyzers.tradeanalyzer.get_analysis()['pnl']['net']['total'],
                                "average": strat.analyzers.tradeanalyzer.get_analysis()['pnl']['net']['average'],
                            }

                        key = tuple(  # Dict's key is a tuple containing strat parameters
                            list(
                                dict(strat.params._getkwargs()).items()))

                        pnls_dict[key] = pnl_dict

                pnls[symbol] = sorted(pnls_dict.items(), key=lambda x: x[1]['total'], reverse=True)[:3]

        return pnls

    def pretty_pnls(self):

        pnl_per_symbol = self.get_top_3_pnls_per_symbol()

        del_params = "logging logger".split(" ")

        for symbol, pnls in pnl_per_symbol.items():

            params_dict = []
            for pnl_dict in pnls:
                pnl_subdict = dict(pnl_dict[0])
                for param in del_params:
                    if param in pnl_subdict:
                        del pnl_subdict[param]
                params_dict.append(pnl_subdict)

            for index, subdict in enumerate(params_dict):
                print("\n")
                print(f"Strat {index+1} : ", symbol)
                for param, value in subdict.items():
                    print(param, value)
                print(f"\nTotal PNL : {pnls[index][1]['total']}")
                print(f"Average PNL : {pnls[index][1]['average']}")

    def print_metrics(self):

        for symbol, result in self.results.items():

            if type(result[0]) is not list:
                print(symbol)
                print(tuple(  # Dict's key is a tuple containing strat parameters
                    list(
                        dict(strat.params._getkwargs()).items())))
                metrics = result[0].analyzers.full_metrics.get_analysis()
                self._metrics_display(metrics)

            else:
                for res in result:  # For loop for iterating in all strats
                    for strat in res:
                        print(symbol)
                        print(tuple(  # Dict's key is a tuple containing strat parameters
                            list(
                                dict(strat.params._getkwargs()).items())))
                        metrics = strat.analyzers.full_metrics.get_analysis()
                        self._metrics_display(metrics)



    @staticmethod
    def _metrics_display(metrics):
        metrics_list = []
        for k, v in metrics.items():

            if isinstance(v, float):
                v = round(v, 2)

            if k in "Annual returns, Average drawdown, Max drawdown, Returns volatility, Average return per trade, Average return per long, " \
                    "Average return per short, Winrate".split(", "):
                v = f"{v} %"

            color = "white"
            if k in "Annual returns, PNL net, Fees, Winrate".split(", "):
                color = "green"
            if k in "Average return per trade, Total trades, Total long, Total short, Open trades, Average return per long, Average return per short".split(
                    ", "):
                color = "blue"
            if k in "Time in market, Average trade len, Max trade len, Average won len, Average lost len".split(", "):
                color = "magenta"
            if k in "Average drawdown, Average drawdown length, Max drawdown, Max drawdown length".split(", "):
                color = "red"
            if k in "Annualized Sharpe ratio, Returns volatility, Calmar ratio".split(", "):
                color = "yellow"
            k, v = colored(k, color, attrs=["bold"]), colored(v, color)

            metrics_list.append([k, v])

        print(tabulate(metrics_list, tablefmt="grid"))