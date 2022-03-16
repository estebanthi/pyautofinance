import random
import pandas as pd
import numpy as np


class MonteCarloSimulator:

    def __init__(self, trades_collection):
        self._trades_collection = trades_collection

    def simulate_n_times(self, number_of_simulations, starting_equity, ending_equity):
        results = []

        for n in range(number_of_simulations):
            random.shuffle(self._trades_collection)
            simulation_result = self.simulate(self._trades_collection, starting_equity, ending_equity)
            results.append(simulation_result)

        dataframe = pd.DataFrame({
            'ruined': [r[0] for r in results],
            'max_drawdown': [r[1] for r in results],
            'profit': [r[2] for r in results],
            'returns': [r[3] for r in results],
            'returns_drawdown': [r[4] for r in results]
        })

        print(dataframe['profit'].mean())


    def simulate(self, trades, starting_equity, ending_equity):
        equities = [starting_equity]
        for trade in trades:
            equity_change = 1+trade.pnl_percent/100
            last_equity = equities[-1]
            new_equity = last_equity*equity_change
            equities.append(new_equity)
            if new_equity < ending_equity:
                break

        final_equity = equities[-1]

        ruined = final_equity < ending_equity
        max_drawdown = self.calculate_max_drawdown(equities)
        profit = final_equity - starting_equity
        returns = final_equity / starting_equity
        return_drawdown = returns / max_drawdown

        return ruined, max_drawdown, profit, returns, return_drawdown

    def calculate_max_drawdown(self, equities):
        drawdown_low_index = np.argmax(np.maximum.accumulate(equities) - equities)  # end of the period
        drawdown_peak_index = np.argmax(equities[:drawdown_low_index])

        low = equities[drawdown_low_index]
        peak = equities[drawdown_peak_index]

        drawdown = (peak - low) / peak
        return drawdown
