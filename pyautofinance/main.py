import pandas as pd
import numpy as np
import pandas_ta as ta
import datetime as dt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


def test():
    n = 5

    df = pd.read_csv('data/BTC-EUR 2019-01-01 00-00-00 2022-03-15 00-00-00 1h.csv')

    df['min'] = df['min'].fillna(0)
    df['max'] = df['max'].fillna(0)

    has_met_min = 0
    signals = []
    profits = []
    open_price = 0
    close_price = 0
    for index, row in df.iterrows():
        signal = 0
        profit = 0
        if has_met_min and row['max'] != 0:
            has_met_min = 0
            close_price = row['Close']
            profit = close_price - open_price
            profit *= 0.96
        if not has_met_min and row['min'] != 0:
            has_met_min = 1
            open_price = row['Close']
        if has_met_min:
            signal = 1
        signals.append(signal)
        profits.append(profit)

    df['Signal'] = signals

    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index)
    df = df[~df.index.duplicated(keep='first')]
    df.ta.strategy('All')

    na_values = []
    for col in df:
        na_values.append((col, df[col].isna().sum()))

    na_values.sort(key=lambda x: x[1], reverse=True)

    cols_to_drop = []
    for col in na_values:
        if col[1] > 100:
            cols_to_drop.append(col[0])

    df.drop(columns=cols_to_drop, inplace=True)
    df.dropna(inplace=True)

    X = df.drop(columns=['Signal'])
    Y = df['Signal']

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, shuffle=False)

    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print(classification_report(y_test, y_pred))

if __name__ == '__main__':
    test()
