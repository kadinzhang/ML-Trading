import pandas as pd
# from util import get_data, plot_data
from util import get_data, plot_data

def normalize_data(df):
    df = df / df.iloc[0]
    return df

def test_run():
    # Get data
    dates = pd.date_range("2019-11-01", "2020-03-26")
    symbols = ["ZM", "TSLA", "COST", "SPY", "UAL", "AAPL", "GOOG"]
    df = get_data(symbols, dates)

    # Plot data
    df = normalize_data(df)
    plot_data(
        df,
        title="Normalized Stock Prices",
        xlabel="Date",
        ylabel="Normalized Adjusted Close Price",
    )

if __name__ == "__main__":
    test_run()
