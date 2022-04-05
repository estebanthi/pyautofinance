import random
import numpy as np

from pyautofinance.common.metrics.monte_carlo_metrics import RiskOfRuin, MaxDrawdownFromEquity, MedianMaxDrawdown
from pyautofinance.common.metrics.monte_carlo_metrics import MedianProfit, MedianReturn, ReturnDrawdown
from pyautofinance.common.metrics.metrics_collection import MetricsCollection


class MonteCarloSimulator:

    def __init__(self, number_of_simulations, starting_equity, ending_equity):
        self.number_of_simulations = number_of_simulations
        self.starting_equity = starting_equity
        self.ending_equity = ending_equity

    def simulate(self, engine):
        engine_result = engine.run()

        strat_results_metrics = []
        for strat_result in engine_result:
            results = self._get_results(strat_result.trades)
            metrics = self._build_metrics(results)
            collection = MetricsCollection(*metrics)

            strat_results_metrics.append(collection)

        return strat_results_metrics

    def _get_results(self, trades_collection):
        results = []
        for n in range(self.number_of_simulations):
            random.shuffle(trades_collection)
            simulation_result = self._simulate(trades_collection)
            results.append(simulation_result)
        return results

    def _simulate(self, trades):
        equities = [self.starting_equity]
        for trade in trades:
            equity_change = 1 + trade.pnl_percent / 100
            last_equity = equities[-1]
            new_equity = last_equity * equity_change
            equities.append(new_equity)
            if new_equity < self.ending_equity:
                break

        final_equity = equities[-1]

        ruined = int(final_equity < self.ending_equity)
        max_drawdown = MaxDrawdownFromEquity(equities).value
        profit = final_equity - self.starting_equity
        returns = final_equity / self.starting_equity
        return_drawdown = returns / max_drawdown

        return [ruined, max_drawdown, profit, returns, return_drawdown]

    def _build_metrics(self, results):
        results_array = np.array(results)

        ruined = results_array[:, 0]
        risk_of_ruin = RiskOfRuin(ruined)

        max_drawdowns = results_array[:, 1]
        median_max_drawdown = MedianMaxDrawdown(max_drawdowns)

        profits = results_array[:, 2]
        median_profit = MedianProfit(profits)

        returns = results_array[:, 3]
        median_return = MedianReturn(returns)

        return_drawdown = ReturnDrawdown(median_return.value, median_max_drawdown.value)

        return risk_of_ruin, median_max_drawdown, median_profit, median_return, return_drawdown
