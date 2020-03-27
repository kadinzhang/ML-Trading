import os
import pandas as pd
import matplotlib.pyplot as plt
import requests
import Historical_Data as hd

def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol.
    If CSV is not already downloaded, will download from yahoo finance """
    # print("Symbol to path, " + symbol)


    if os.path.exists(os.path.join(base_dir, "{}.csv".format(str(symbol)))) == False:
        hd.pull_specific_stocks([symbol])
    
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))



def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    df = df.loc[start_index:end_index, columns]
    plot_data(df)


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if "SPY" not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, "SPY")

    for symbol in symbols:
        df_temp = pd.read_csv(
            symbol_to_path(symbol),
            index_col="Date",
            parse_dates=True,
            usecols=["Date", "Adj Close"],
            na_values=["nan"],
        )
        company_name = get_symbol(symbol)

        df_temp = df_temp.rename(columns={"Adj Close": company_name})

        df = df.join(df_temp)

        if company_name == "SPDR S&P 500 ETF Trust":
            df = df.dropna(subset=["SPDR S&P 500 ETF Trust"])

    return df


def test_run():
    # Define a date range
    dates = pd.date_range("2019-11-01", "2020-03-26")

    # Choose stock symbols to read
    symbols = ["SPY", "TSLA", "ZM", "COST", "UAL"]

    # Get stock data
    df = get_data(symbols, dates)

    plot_data(df)

    # plot_data(normalize_data(df))


def normalize_data(df):
    df = df / df.iloc[0]
    return df


def plot_data(df, title="Stock Prices"):
    ax = df.plot(title=title, fontsize=10)
    ax.set_xlabel("Date")
    ax.set_ylabel("Adjusted Close Price (USD)")
    plt.show()


def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(
        symbol
    )

    result = requests.get(url).json()

    for x in result["ResultSet"]["Result"]:
        if x["symbol"] == symbol:
            return x["name"]


if __name__ == "__main__":
    test_run()
