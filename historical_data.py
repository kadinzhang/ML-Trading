import urllib.request
import time
import math
import os
import shutil


# period1 and period2 are Unix time stamps for your start and end date
# interval is the data retrieval interval (this can be either 1d, 1w or 1m)


def pull_all_data():
    with open("old_data/Lists/sp5002012.txt", "r") as file:
        for line in file:
            company = line.strip()
            print(company)
            print("\n")
            pull_historical_data(company)
            try:
                filename = make_filename((company))
                src = os.getcwd()
                dst = src + "/data"
                shutil.move(os.path.join(src, filename), os.path.join(dst, filename))
            except:
                print("Error moving file")


def pull_specific_stocks(stocks):
    """Download data of specific stocks from yahoo finance"""
    for stock in stocks:

        print("Downloading historical data for: " + stock)
        pull_historical_data(stock)

        try:
            filename = make_filename((stock))
            src = os.getcwd()
            dst = src + "/data"
            shutil.move(os.path.join(src, filename), os.path.join(dst, filename))
        except Exception as e:
            print("Error moving file")
            print(e)


current_time = str(math.floor(time.time()))

# Times:
# 2019-01-01 : 1546300800
# 2000-01-01 : 946684800


def make_url(
    ticker_symbol, period1="1546300800", period2=current_time, interval="1d",
):

    return "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval={}&events=history".format(
        ticker_symbol, period1, period2, interval
    )


def make_filename(ticker_symbol):
    return ticker_symbol + ".csv"


def pull_historical_data(ticker_symbol):
    try:
        urllib.request.urlretrieve(
            make_url(ticker_symbol), make_filename(ticker_symbol)
        )
    # except urllib.request.ContentTooShortError as e:
    #     outfile = open(make_filename(ticker_symbol, directory), "w")
    #     outfile.write(e.content)
    #     outfile.close()
    except:
        print("Error Fetching stock, may not exist")


if __name__ == "__main__":
    # pull_all_data()
    stocks = ["ZM", "GOOG", "UAL"]
    pull_specific_stocks(stocks)
