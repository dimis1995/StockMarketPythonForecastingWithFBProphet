import config
import requests
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt


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


if __name__ == '__main__':

    picked_columns = ['open', 'high', 'low', 'close', 'volume']

    model_and_predict(pd.read_csv('AAPL.csv'), 'Apple', picked_columns)
    model_and_predict(pd.read_csv('MSFT.csv'), 'Microsoft', picked_columns)
    model_and_predict(pd.read_csv('IBM.csv'), 'IBM', picked_columns)

    plt.show()
