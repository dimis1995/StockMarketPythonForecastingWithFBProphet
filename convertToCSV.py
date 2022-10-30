# replace the name with your json downloaded from
# https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=demo
# when the program is finished, go to the csv and name the first column as Date

import json
import pandas as pd

if __name__ == '__main__':
    file = open('IBMDaily.json')
    IBM = json.load(file)
    file.close()
    IBM = IBM['Time Series (Daily)']
    IBM = pd.DataFrame(IBM)
    IBM = IBM.transpose()
    dict = {'': 'Date', '1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close',
            '5. volume': 'volume'}
    IBM.rename(columns=dict, inplace=True)
    IBM.to_csv('IBM.csv')