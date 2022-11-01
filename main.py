import config
import requests
import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt
from datetime import date, datetime


def business_days_difference(date_in_api: str, date_in_dataset: str) -> int:
    date1 = datetime.strptime(date_in_api, "%Y-%m-%d")
    try:
        date2 = datetime.strptime(date_in_dataset, "%m/%d/%Y")
    except:
        date2 = datetime.strptime(date_in_dataset, "%Y-%m-%d")
    return np.busday_count(date2.strftime('%Y-%m-%d'),
                           date1.strftime('%Y-%m-%d'))


def model_and_predict(dataset: pd.DataFrame, title: str, columns: [str]):
    for column in columns:
        changed_names = {'Date': 'ds', column: 'y'}
        dataset_copy = dataset.rename(columns=changed_names)

        model = Prophet()
        model.fit(dataset_copy)
        future = model.make_future_dataframe(periods=365)
        forecast = model.predict(future)

        fig = model.plot(forecast, ylabel=column, xlabel='Time', include_legend=True)
        ax = fig.gca()
        ax.set_title(title, size=6)


def update_if_needed(path: str, symbol: str):
    dataset = pd.read_csv(path)
    if str(date.today()) != dataset['Date'][0]:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&apikey='
        url += config.MY_API
        response = requests.get(url)
        response_json = response.json()
        response_json = response_json['Time Series (Daily)']
        days = list(response_json.keys())
        if days[0] != dataset['Date'][0]:
            difference = business_days_difference(days[0], dataset['Date'][0])
            if difference > 0:
                new_entries = []
                for i in range(0, difference):
                    entry = response_json[days[i]]
                    new_entries.append([days[i],
                                        entry['1. open'],
                                        entry['2. high'],
                                        entry['3. low'],
                                        entry['4. close'],
                                        entry['5. volume']])
                for entry in reversed(new_entries):
                    try:
                        dataset.loc[-1] = entry
                        dataset.index = dataset.index + 1
                        dataset = dataset.sort_index()
                    except ValueError:
                        if dataset.columns[0] == '':
                            new_entry = [0, entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]]
                            dataset.loc[-1] = new_entry
                            dataset.index = dataset.index + 1
                            dataset = dataset.sort_index()
                dataset['Date'] = pd.to_datetime(dataset['Date'])
                dataset.to_csv(path)


if __name__ == '__main__':
    picked_columns = ['open', 'high', 'low', 'close', 'volume']

    update_if_needed('AAPL.csv', 'AAPL')
    update_if_needed('MSFT.csv', 'MSFT')
    update_if_needed('IBM.csv', 'IBM')

    model_and_predict(pd.read_csv('AAPL.csv'), 'Apple', picked_columns)
    model_and_predict(pd.read_csv('MSFT.csv'), 'Microsoft', picked_columns)
    model_and_predict(pd.read_csv('IBM.csv'), 'IBM', picked_columns)

    plt.show()
