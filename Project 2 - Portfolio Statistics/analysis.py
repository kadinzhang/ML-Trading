import os
import sys

sys.path.insert(0, os.path.dirname(os.getcwd()))

from util import *


def portfolio_statistics(
        start_date,
        end_date,
        symbols,
        allocations,
        start_value,
        risk_free_rate,
        sample_frequency,
):
    # Get and fill data
    dates = pd.date_range(start_date, end_date)
    prices = get_data(symbols, dates)
    print(prices)
    prices.fillna(method="ffill", inplace=True)
    prices.fillna(method="bfill", inplace=True)
    prices = prices[symbols]

    # Calculate portfolio values
    normed = prices / prices.values[0]
    alloced = normed * allocations
    pos_values = alloced * start_value
    port_vals = pos_values.sum(axis=1)

    # Calculate daily returns
    daily_rets = (port_vals[1:] / port_vals.values[:-1]) - 1

    # Calculate portfolio statistics
    cumulative_return = (port_vals[-1] / port_vals[0]) - 1
    average_daily_return = daily_rets.mean()
    risk = daily_rets.std()
    sharpe_ratio = (daily_rets - risk_free_rate).mean() / risk

    return cumulative_return, average_daily_return, risk, sharpe_ratio


if __name__ == "__main__":
    cumulative_return, average_daily_return, risk, sharpe_ratio = portfolio_statistics(
        "2010-01-22",
        "2010-02-22",
        ["GOOG", "AAPL", "GLD", "TSLA"],
        [0.3, 0.3, 0.2, 0.2],
        100000,
        0,
        252,
    )

    print("Cumulative return: ", cumulative_return)
    print("Average daily return: ", average_daily_return)
    print("Risk: ", risk)
    print("Sharpe ratio: ", sharpe_ratio)
