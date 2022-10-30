import config
import requests
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey='
    # url += config.MY_API
    # response = requests.get(url)

    columns = ['open', 'high', 'low', 'close', 'volume']

    aapl = pd.read_csv('AAPL.csv')
    for column in columns:
        if column == 'Date':
            continue
        dict = {'Date':'ds', column: 'y'}
        aapl_copy = aapl.rename(columns=dict)

        model = Prophet()
        model.fit(aapl_copy)
        future = model.make_future_dataframe(periods=365)
        forecast = model.predict(future)

        fig = model.plot(forecast, ylabel=column, xlabel='Time', include_legend=True)
        ax = fig.gca()
        ax.set_title('Apple', size=6)

    msft = pd.read_csv('MSFT.csv')
    for column in columns:
        if column == 'Date':
            continue
        dict = {'Date': 'ds', column: 'y'}
        msft_copy = msft.rename(columns=dict)

        model = Prophet()
        model.fit(msft_copy)
        future = model.make_future_dataframe(periods=365)
        forecast = model.predict(future)

        fig = model.plot(forecast, ylabel=column, xlabel='Time', include_legend=True)
        ax = fig.gca()
        ax.set_title('Microsoft', size=6)

    ibm = pd.read_csv('IBM.csv')
    for column in columns:
        if column == 'Date':
            continue
        dict = {'Date': 'ds', column: 'y'}
        ibm_copy = ibm.rename(columns=dict)

        model = Prophet()
        model.fit(ibm_copy)
        future = model.make_future_dataframe(periods=365)
        forecast = model.predict(future)

        fig = model.plot(forecast, ylabel=column, xlabel='Time', include_legend=True)
        ax = fig.gca()
        ax.set_title('Apple', size=6)

    plt.show()
