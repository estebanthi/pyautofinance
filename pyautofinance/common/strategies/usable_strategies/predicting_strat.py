from backtrader.indicators import ExponentialMovingAverage

from pyautofinance.common.strategies.bracket_strategy import BracketStrategy


class PredictingStrat(BracketStrategy):
    params = (
        ('predicter', None),
        ('update_predicter', False),
        ('train_period', 0),
        ('ema_period', 100),
    )

    def _init_indicators(self):
        self.prediction = 0
        self.ema = ExponentialMovingAverage(period=self.p.ema_period)

    def _update_attributes(self):
        self.prediction = 0
        if len(self) > self.p.train_period:
            try:
                strat_df = self.get_ohlcv_dataframe()
                if self.p.update_predicter: self.p.predicter.fit(strat_df)
                self.prediction = self.p.predicter.predict(strat_df)[-1]
            except Exception as e:
                print(e)

    def _open_long_condition(self) -> bool:
        return self.prediction == 1 and self.datas[0].close[0] > self.ema[0]

    def _open_short_condition(self) -> bool:
        return self.prediction == -1 and self.datas[0].close[0] < self.ema[0]

    def _close_short_condition(self) -> bool:
        return self.prediction != -1

    def _close_long_condition(self) -> bool:
        return self.prediction != 1
