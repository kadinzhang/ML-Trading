import urllib.request
import time
import math
#  https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1497727945&period2=1500319945&interval=1d&events=history&crumb=C9luNcNjVkK
# Let's examine how ths URL is constructed.

# period1 and period2 are Unix time stamps for your start and end date
# interval is the data retrieval interval (this can be either 1d, 1w or 1m)
# crumb is an alphanumeric code that’s periodically regenerated every time
# you download new historical data from from the Yahoo Finance website using
# your browser. Moreover, crumb is paired with a cookie that’s stored by your
# browser.

current_time = str(math.floor(time.time()))
def make_url(
    ticker_symbol,
    period1="946684800",
    period2=current_time,
    interval="1d",
):

    return "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval={}&events=history".format(
        ticker_symbol, period1, period2, interval
    )


output_path = "C:/Users/sebal/Desktop/Coding/Python/ML-Trading/"


def make_filename(ticker_symbol, directory="S&P"):
    # return output_path + "/" + directory + "/" + ticker_symbol + ".csv"
    return ticker_symbol + ".csv"


def pull_historical_data(ticker_symbol, directory="S&P"):
    try:
        urllib.request.urlretrieve(
            make_url(ticker_symbol), make_filename(ticker_symbol, directory)
        )
    except urllib.request.ContentTooShortError as e:
        outfile = open(make_filename(ticker_symbol, directory), "w")
        outfile.write(e.content)
        outfile.close()


pull_historical_data("AAPL")
