import pandas as pd
import scipy.optimize as spo
from util import get_data



def optimize_portfolio(start_date, end_date, symbols, criteria):
    # Get and fill data
    dates = pd.date_range(start_date, end_date)
    prices = get_data(symbols, dates, addSPY=False)
    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='bfill', inplace=True)




def test_run():
    return


if __name__ == "__main__":
    test_run()