# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn; seaborn.set()
from datetime import date

tweets = pd.read_json('james_franco_lex_pol.json')
tweets.sort_values(by='timestamp', inplace=True)
tweets.where(tweets['timestamp'])

startDate = date(2017, 12, 15)
endDate = date(2018, 2, 15)

# https://stackoverflow.com/questions/41783003/how-do-i-convert-timestamp-to-datetime-date-in-pandas-dataframe
tweets['timestamp'] = pd.to_datetime(tweets['timestamp']).apply(lambda x: x.date())

tweets_stub = tweets[tweets['timestamp'] >= startDate]
tweets_stub = tweets_stub[tweets_stub['timestamp'] <= endDate]
tweets_stub.sort_values(by='timestamp', inplace=True)

tweets_date_grouped = tweets_stub.groupby(by=['timestamp','lexicon_polarity']).count()['text']