import pandas as pd
from util import get_data


def portfolio_statistics(start_date, end_date, symbols, allocations, start_value, risk_free_rate, sample_frequency):
    dates = pd.date_range(start_date, end_date)
    prices = get_data(symbols, dates)

    prices.fillna(method="ffill", inplace=True)
    prices.fillna(method="bfill", inplace=True)

    prices = prices[symbols]
    # normed = prices / prices[0]
    print(prices.mean())
    return


portfolio_statistics('2010-01-22', '2010-02-22', ['GOOG', 'AAPL', 'GLD', 'XOM'], [0.3, 0.3, 0.2, 0.2], 100000, 0, 252)
