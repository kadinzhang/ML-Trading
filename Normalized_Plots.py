import os
import pandas as pd
import matplotlib.pyplot as plt

def symbol_to_path(symbol, base_dir="current_data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    df = df.loc[start_index : end_index, columns]
    plot_data(df)

def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')
    
    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), 
        index_col="Date", 
        parse_dates = True,
        usecols =["Date", "Adj Close"],
        na_values = ["nan"]
        )
       
        df_temp = df_temp.rename(columns={"Adj Close" : symbol})
        df = df.join(df_temp)
        
        if symbol == "SPY":
            df = df.dropna(subset=['SPY'])
    return df


def test_run():
    # Define a date range
    dates = pd.date_range('2019-01-01', '2020-03-26')

    # Choose stock symbols to read
    symbols = ['SPY', 'GOOG', 'AAPL', 'IBM']
    
    # Get stock data
    df = get_data(symbols, dates)

    plot_data(normalize_data(df))

def normalize_data(df):
    df = df / df.iloc[0]
    return df

def plot_data(df, title = 'Stock Prices'):
    ax = df.plot(title=title, fontsize=10)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.show()

if __name__ == "__main__":
    test_run()
