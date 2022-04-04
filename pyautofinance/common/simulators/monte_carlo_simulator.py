import random
import pandas as pd

from pyautofinance.common.metrics.monte_carlo_metrics import RiskOfRuin, MaxDrawdownFromEquity, AverageMaxDrawdown,\
    AverageReturns, AverageProfit, AverageReturnsDrawdown


class MonteCarloSimulator:

    def __init__(self, number_of_simulations, starting_equity, ending_equity):
        self.number_of_simulations = number_of_simulations
        self.starting_equity = starting_equity
        self.ending_equity = ending_equity

    def simulate(self, trades_collection):
        results = self._get_results(trades_collection)
        results_dataframe = self._build_results_dataframe(results)

        risk_of_ruin = RiskOfRuin(results_dataframe)
        average_max_drawdown = AverageMaxDrawdown(results_dataframe)
        average_profit = AverageProfit(results_dataframe)
        average_returns = AverageReturns(results_dataframe)
        average_returns_drawdown = AverageReturnsDrawdown(results_dataframe)
        return {
            'risk_of_ruin': risk_of_ruin,
            'average_max_drawdown': average_max_drawdown,
            'average_profit': average_profit,
            'average_returns': average_returns,
            'average_returns_drawdown': average_returns_drawdown
        }

    def _get_results(self, trades_collection):
        results = []
        for n in range(self.number_of_simulations):
            random.shuffle(trades_collection)
            simulation_result = self._simulate(trades_collection)
            results.append(simulation_result)
        return results

    @staticmethod
    def _build_results_dataframe(results):
        return pd.DataFrame({
            'ruined': [r[0] for r in results],
            'max_drawdown': [r[1] for r in results],
            'profit': [r[2] for r in results],
            'returns': [r[3] for r in results],
            'returns_drawdown': [r[4] for r in results]
        })

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

        ruined = final_equity < self.ending_equity
        max_drawdown = MaxDrawdownFromEquity(equities).value
        profit = final_equity - self.starting_equity
        returns = final_equity / self.starting_equity
        return_drawdown = returns / max_drawdown

        return ruined, max_drawdown, profit, returns, return_drawdown

