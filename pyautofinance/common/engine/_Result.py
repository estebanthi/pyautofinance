from termcolor import colored
from tabulate import tabulate


class _Result:

    def __init__(self, engine_result):
        self._result = engine_result

    def get(self):
        return self._result

    def get_top_x_pnl(self, number_to_get):  # TradeAnalyzer is needed
        pnls = {}

        for symbol, result in self._result.items():
            pnls[symbol] = self._get_top_x_pnls_for_symbol(result, number_to_get)

        return pnls

    def _get_top_x_pnls_for_symbol(self, result, number_to_get):
        pnls_dict = {}
        for res in result:  # For iterating in all strats
            for strat in res:
                pnl_dict = self._get_pnl_from_strat(strat)
                key = self._get_key_from_strat(strat)
                pnls_dict[key] = pnl_dict

        return sorted(pnls_dict.items(), key=lambda x: x[1]['total'], reverse=True)[:number_to_get]

    @staticmethod
    def _get_pnl_from_strat(strat):
        analysis = strat.analyzers.tradeanalyzer.get_analysis()

        pnl_dict = {
            "total": 0,
            "average": 0,
        }

        if "pnl" in analysis:
            pnl_dict = {
                "total": analysis['pnl']['net']['total'],
                "average": analysis['pnl']['net']['average'],
            }

        return pnl_dict

    @staticmethod
    def _get_key_from_strat(strat):
        return tuple(
            list(
                dict(strat.params._getkwargs()).items()))

    def pretty_pnls(self):

        pnl_per_symbol = self.get_top_3_pnls_per_symbol()

        params_to_del = "logging logger".split(" ")

        for symbol, pnls in pnl_per_symbol.items():

            params_dict = []
            for pnl_dict in pnls:
                params = self._get_params_from_pnl_dict(pnl_dict)
                self._del_params_to_del_in_params(params, params_to_del)
                params_dict.append(params)

            for index, subdict in enumerate(params_dict):
                print("\n")
                self._diplay_strat_at_index(index, symbol)
                self._display_params(subdict)
                self._display_pnl_at_index(pnls, index)

    @staticmethod
    def _get_params_from_pnl_dict(pnl_dict):
        return dict(pnl_dict[0])

    @staticmethod
    def _del_params_to_del_in_params(params, params_to_del):
        for param in params_to_del:
            if param in params:
                del params[param]

    @staticmethod
    def _diplay_strat_at_index(index, symbol):
        print(f"Strat {index + 1} : ", symbol)

    @staticmethod
    def _display_params(subdict):
        for param, value in subdict.items():
            print(param, value)

    @staticmethod
    def _display_pnl_at_index(pnls, index):
        print(f"\nTotal PNL : {pnls[index][1]['total']}")
        print(f"Average PNL : {pnls[index][1]['average']}")

    def print_metrics(self):

        for symbol, result in self._result.items():
            for res in result:
                for strat in res:
                    self._display_everything(strat, symbol)

    def _display_everything(self, strat, symbol):
        print(symbol)
        params = self._get_key_from_strat(strat)
        print(params)
        metrics = strat.analyzers.full_metrics.get_analysis()
        self._metrics_display(metrics)

    def _metrics_display(self, metrics):
        metrics_list = []

        percent_metrics = "Annual returns, Average drawdown, Max drawdown, Returns volatility," \
                          " Average return per trade, Average return per long, " \
                          "Average return per short, Winrate".split(", ")

        to_display_in_green = "Annual returns, PNL net, Fees, Winrate".split(", ")

        to_display_in_blue = "Average return per trade, Total trades, Total long, Total short, Open trades," \
                             " Average return per long, Average return per short".split(", ")

        to_display_in_magenta = "Time in market, Average trade len, Max trade len, Average won len," \
                                " Average lost len".split(", ")

        to_display_in_red = "Average drawdown, Average drawdown length, Max drawdown," \
                            " Max drawdown length".split(", ")

        to_display_in_yellow = "Annualized Sharpe ratio, Returns volatility, Calmar ratio".split(", ")

        default_color = 'white'

        for key, value in metrics.items():

            value = self._round_value_if_is_float(value, 2)

            if key in percent_metrics:
                value = self._format_value_to_percent_str(value)

            color = self._get_color_from_key(key, default_color, to_display_in_green, to_display_in_blue,
                                             to_display_in_magenta, to_display_in_red, to_display_in_yellow)

            key, value = colored(key, color, attrs=["bold"]), colored(value, color)
            metrics_list.append([key, value])

        print(tabulate(metrics_list, tablefmt="grid"))

    @staticmethod
    def _round_value_if_is_float(value, decimals=2):
        if isinstance(value, float):
            return round(value, decimals)

    @staticmethod
    def _format_value_to_percent_str(value):
        return f"{value} %"

    @staticmethod
    def _get_color_from_key(key, default_color, to_display_in_green, to_display_in_blue,
                            to_display_in_magenta, to_display_in_red, to_display_in_yellow):
        color = default_color

        if key in to_display_in_green:
            color = "green"

        if key in to_display_in_blue:
            color = "blue"

        if key in to_display_in_magenta:
            color = "magenta"

        if key in to_display_in_red:
            color = "red"

        if key in to_display_in_yellow:
            color = "yellow"

        return color

    def get_best_params(self):
        best_params_per_symbol = {}
        for symbol, result in self._result.items():
            initial_strat = result[0][0]
            max_pnl = initial_strat.analyzers.tradeanalyzer.get_analysis().pnl.net.total
            best_params = self._get_params_dict_from_strat(initial_strat)

            for res in result:
                for strat in res:
                    pnl = strat.analyzers.tradeanalyzer.get_analysis().pnl.net.total
                    if pnl > max_pnl:
                        max_pnl = pnl
                        best_params = self._get_params_dict_from_strat(strat)
            best_params_per_symbol[symbol] = best_params
            return best_params_per_symbol

    def _get_params_dict_from_strat(self, strat):
        key = self._get_key_from_strat(strat)
        params = {}
        for param in key:
            param_name = param[0]
            param_value = param[1]
            params[param_name] = param_value
        return params
