import config
import requests
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from datetime import date, datetime


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
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+symbol+'&apikey='
        url += config.MY_API
        response = requests.get(url)
        response_json = response.json()
        response_json = response_json['Time Series (Daily)']
        days = list(response_json.keys())
        if days[0] != dataset['Date'][0]:
            last_day = dataset['Date'][0]
            try:
                last_day = datetime.strptime(last_day, "%m/%d/%Y")
            except:
                last_day = datetime.strptime(last_day, "%Y-%m-%d")
            difference = datetime.strptime(days[0], "%Y-%m-%d") - last_day
            if difference.days > 0:
                new_entries = []
                for i in range(0, difference.days):
                    entry = response_json[days[i]]
                    new_entries.append([days[i],
                                        entry['1. open'],
                                        entry['2. high'],
                                        entry['3. low'],
                                        entry['4. close'],
                                        entry['5. volume']])
                for entry in reversed(new_entries):
                    dataset.loc[-1] = entry
                    dataset.index = dataset.index+1
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
