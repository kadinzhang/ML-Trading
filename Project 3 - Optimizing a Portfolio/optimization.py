import pandas as pd
import scipy.optimize as spo
import numpy as np
import datetime as dt
from util import get_data, plot_data

def f(normed, allocs, sv):
    # Function to be minimized
    alloced = normed * allocs
    pos_val = alloced * sv
    port_val = pos_val.sum(axis = 1)
    daily_rets = (port_val[1:]/port_val.values[:-1]) - 1
    risk = daily_rets.std()
    cr = -(port_val[-1] / port_val.values[0]) - 1
    sr = (daily_rets - 0.0).mean() / risk
    return risk



def optimize_portfolio(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), syms=['GOOG', 'AAPL', 'GLD', 'XOM'], gen_plot=False):
    sv = 1000000
    rfr = 0.0

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)
    prices = prices_all[syms]
    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='bfill', inplace=True)
    prices_SPY = prices_all['SPY']

    # Find allocations with optimization
    n = len(syms)
    normed = prices / prices.values[0]
    guess = [1.0/n] * n
    bounds = [(0.0, 1.0) for i in normed.columns]
    constraints = ({'type': 'eq', 'fun': lambda inputs: 1.0 - np.sum(inputs)})
    minimize_result = spo.minimize(f, guess, args=(normed, sv), method='SLSQP', constraints=constraints, bounds=bounds, options={'disp': True})
    allocs = minimize_result.x

    # Calculate portfolio statistics
    alloced = normed * allocs
    pos_val = alloced * sv
    port_val = pos_val.sum(axis=1)
    daily_rets = (port_val[1:] / port_val.values[:-1]) - 1
    cr = (port_val[-1] / port_val.values[0]) - 1
    adr = daily_rets.mean()
    sddr = daily_rets.std()
    sr = (daily_rets - rfr).mean() / sddr

    # Compare daily portfolio value with SPY using a normalized plot  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    if gen_plot:
        prices_SPY = prices_SPY / prices_SPY.values[0]
        port_val = port_val / port_val.values[0]
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp, title="Risk-optimized portfolio and SPY performance")

    return allocs, cr, adr, sddr, sr


def test_code():
    start_date = dt.datetime(2020, 1, 1)
    end_date = dt.datetime(2020, 3, 30)
    symbols = ['GOOG', 'AAPL', 'GLD', 'ZM', 'COST', 'UAL']

    # Assess the portfolio  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd=start_date, ed=end_date, \
                                                        syms=symbols, \
                                                        gen_plot=True)

    # Print statistics  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Symbols: {symbols}")
    print(f"Allocations:{allocations}")
    print(f"Sharpe Ratio: {sr}")
    print(f"Volatility (stdev of daily returns): {sddr}")
    print(f"Average Daily Return: {adr}")
    print(f"Cumulative Return: {cr}")


if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
