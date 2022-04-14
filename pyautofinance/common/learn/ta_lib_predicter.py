from scipy.signal import argrelextrema
import pandas as pd
import numpy as np

from pyautofinance.common.learn.predicter import Predicter


class TaLibPredicter(Predicter):

    def _copy(self, other):
        self._model = other._model
        self.ta_strategy = other.ta_strategy
        self._dataframe = other._dataframe

    def _init_predicter(self, model, ta_strategy):
        self._model = model
        self.ta_strategy = ta_strategy
        self._dataframe = pd.DataFrame()

    def predict(self, back_datafeed, local_extremas_periods=5, max_na_values_per_col=100):
        self._prepare_dataframe(back_datafeed, local_extremas_periods, max_na_values_per_col)
        X = self._get_x()
        y = self._model.predict(X)
        return y

    def fit(self, back_datafeed, local_extremas_periods=5, max_na_values_per_col=100):
        self._prepare_dataframe(back_datafeed, local_extremas_periods, max_na_values_per_col)
        X, y = self._get_x(), self._get_y()
        self._model.fit(X, y)

    def _prepare_dataframe(self, back_datafeed, local_extremas_periods, max_na_values_per_col):
        self._dataframe = self._load_dataframe(back_datafeed)
        self._calculate_local_extremas(local_extremas_periods)
        self._calculate_signals()
        self._format_index()
        self._get_ta_analysis()
        self._drop_na_values(max_na_values_per_col)

    @staticmethod
    def _load_dataframe(back_datafeed):
        back_datafeed.extract()
        return back_datafeed.get_ohlcv().dataframe

    def _calculate_local_extremas(self, local_extremas_periods):
        self._dataframe['min'] = self._dataframe.iloc[argrelextrema(self._dataframe.Close.values, np.less_equal,
                                                                    order=local_extremas_periods)[0]]['Close']
        self._dataframe['max'] = self._dataframe.iloc[argrelextrema(self._dataframe.Close.values, np.greater_equal,
                                                                    order=local_extremas_periods)[0]]['Close']

        self._dataframe['min'] = self._dataframe['min'].fillna(0)
        self._dataframe['max'] = self._dataframe['max'].fillna(0)

    def _calculate_signals(self):
        has_met_min = 0
        signals = []
        for index, row in self._dataframe.iterrows():
            signal = 0
            if has_met_min and row['max'] != 0:
                has_met_min = 0
            if not has_met_min and row['min'] != 0:
                has_met_min = 1
            if has_met_min:
                signal = 1
            signals.append(signal)

        self._dataframe['Signal'] = signals

    def _format_index(self):
        self._dataframe.set_index('Date', inplace=True)
        self._dataframe.index = pd.to_datetime(self._dataframe.index)
        self._dataframe = self._dataframe[~self._dataframe.index.duplicated(keep='first')]

    def _get_ta_analysis(self):
        self._dataframe.ta.strategy(self.ta_strategy)

    def _drop_na_values(self, max_na_values_per_col):
        na_values = self._get_na_values()
        cols_to_drop = self._get_cols_to_drop(na_values, max_na_values_per_col)
        self._dataframe.drop(columns=cols_to_drop, inplace=True)
        self._dataframe.dropna(inplace=True)

    def _get_na_values(self):
        na_values = []
        for col in self._dataframe:
            na_values.append((col, self._dataframe[col].isna().sum()))
        return na_values

    @staticmethod
    def _get_cols_to_drop(na_values, max_na_values_per_col):
        cols_to_drop = []
        for col in na_values:
            if col[1] > 100:
                cols_to_drop.append(col[0])
        cols_to_drop.append('min')
        cols_to_drop.append('max')
        return cols_to_drop

    def _get_x(self):
        return self._dataframe.drop(columns=['Signal'])

    def _get_y(self):
        return self._dataframe['Signal']

    def get_real_outputs(self, back_datafeed, local_extremas_periods=5, max_na_values_per_col=100):
        self._prepare_dataframe(back_datafeed, local_extremas_periods, max_na_values_per_col)
        return self._dataframe['Signal']
