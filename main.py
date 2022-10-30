import config
import requests
import pandas as pd

if __name__ == '__main__':
    url = 'https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey='
    url += config.MY_API

    response = requests.get(url)
    print(response.json())
