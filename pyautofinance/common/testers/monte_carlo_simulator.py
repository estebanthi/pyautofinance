import random
import pandas as pd
import numpy as np


class MonteCarloSimulator:

    def __init__(self, trades_collection):
        self._trades_collection = trades_collection

    def simulate_n_times(self, number_of_simulations, starting_equity, ending_equity):
        results = self._get_results(number_of_simulations, starting_equity, ending_equity)
        results_dataframe = self._build_results_dataframe(results)

        risk_of_ruine = self._calculate_risk_of_ruine(results_dataframe)
        average_max_drawdown = results_dataframe['max_drawdown'].mean()
        average_profit = results_dataframe['profit'].mean()
        average_returns = results_dataframe['returns'].mean()
        average_returns_drawdown = average_returns / average_max_drawdown
        return {
            'risk_of_ruine': risk_of_ruine,
            'average_max_drawdown': average_max_drawdown,
            'average_profit': average_profit,
            'average_returns': average_returns,
            'average_returns_drawdown': average_returns_drawdown
        }

    def _get_results(self, number_of_simulations, starting_equity, ending_equity):
        results = []
        for n in range(number_of_simulations):
            random.shuffle(self._trades_collection)
            simulation_result = self.simulate(self._trades_collection, starting_equity, ending_equity)
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

    def simulate(self, trades, starting_equity, ending_equity):
        equities = [starting_equity]
        for trade in trades:
            equity_change = 1 + trade.pnl_percent / 100
            last_equity = equities[-1]
            new_equity = last_equity * equity_change
            equities.append(new_equity)
            if new_equity < ending_equity:
                break

        final_equity = equities[-1]

        ruined = final_equity < ending_equity
        max_drawdown = self._calculate_max_drawdown(equities)
        profit = final_equity - starting_equity
        returns = final_equity / starting_equity
        return_drawdown = returns / max_drawdown

        return ruined, max_drawdown, profit, returns, return_drawdown

    @staticmethod
    def _calculate_max_drawdown(equities):
        drawdown_low_index = np.argmax(np.maximum.accumulate(equities) - equities)  # end of the period
        drawdown_peak_index = np.argmax(equities[:drawdown_low_index])

        low = equities[drawdown_low_index]
        peak = equities[drawdown_peak_index]

        drawdown = (peak - low) / peak
        return drawdown

    @staticmethod
    def _calculate_risk_of_ruine(results_dataframe):
        ruined = results_dataframe['ruined'][results_dataframe['ruined'] == True]
        return len(ruined) / len(results_dataframe)

