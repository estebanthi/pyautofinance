

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