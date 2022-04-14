from pyautofinance.common.strategies.base_strategy import BaseStrategy


class PredictingStrat(BaseStrategy):

    params = (
        ('predicter', None),
        ('update_predicter', False),
        ('train_period', 0)
    )

    def _init_indicators(self):
        self.prediction = 0

    def _update_attributes(self):
        self.prediction = 0

        if self.p.train_period < len(self):

            try:
                strat_df = self.get_ohlcv_dataframe()
                if self.p.update_predicter: self.p.predicter.fit(strat_df)

                strat_df = self.get_ohlcv_dataframe()
                predictions = self.p.predicter.predict(strat_df)
                self.prediction = predictions[-1]
            except:
                pass

    def _open_long_condition(self) -> bool:
        return self.prediction == 1

    def _open_short_condition(self) -> bool:
        return self.prediction == -1

    def _close_short_condition(self) -> bool:
        return self.prediction != -1

    def _close_long_condition(self) -> bool:
        return self.prediction != 1
