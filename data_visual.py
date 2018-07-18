# -*- coding: utf-8 -*-
import pandas as pd
from matplotlib import pyplot
from datetime import datetime, date

tweets = pd.read_json('james_franco_lex_pol.json')
tweets.sort_values(by='timestamp', inplace=True)
tweets.where(tweets['timestamp'])

startDate = datetime(2017, 12, 1)
endDate = datetime(2018, 2, 15)

def to_datetime(x):
    return datetime.strptime(str(x), '%Y-%m-%d %X')

tweets['timestamp'].apply(lambda x: to_datetime(x))

tweets_stub = tweets(tweets['timestamp'] >= startDate and tweets['timestamp'] <= endDate)

# https://stackoverflow.com/questions/41783003/how-do-i-convert-timestamp-to-datetime-date-in-pandas-dataframe
tweets_stub.to_datetime(tweets_stub['timestamp']).date

# look into https://stackoverflow.com/questions/30689445/datetime64-comparison-in-dataframes