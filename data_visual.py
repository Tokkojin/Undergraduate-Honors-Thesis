# -*- coding: utf-8 -*-
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from datetime import datetime

import sys
import os

sns.set()

if __name__ == '__main__':
    celebrity = sys.argv[1]
    filename = os.getcwd() + '/lex_pol/' + celebrity.replace(' ', '_').lower() + '.json'

    articleDate = input("Article date (mm/dd/yy): ")
    articleDate = datetime.strptime(articleDate, '%m/%d/%y')

    chunk_of_tweets = pd.read_json(filename, date_unit='ms', lines=True, chunksize=1000000000)

    for tweets in chunk_of_tweets:
        df = pd.DataFrame()
        df['text'] = pd.DataFrame.from_dict(tweets.iloc[0]['text'], orient='index')[0].tolist()
        df['timestamp'] = pd.DataFrame.from_dict(tweets.iloc[0]['timestamp'], orient='index')[0].tolist()
        df['lex_polarity'] = pd.DataFrame.from_dict(tweets.iloc[0]['lex_polarity'], orient='index')[0].tolist()

        df['timestamp'] = df['timestamp'].apply(lambda ms: datetime.fromtimestamp(ms/1000.0))
        df.sort_values(by='timestamp', inplace=True)
        df = df.groupby(['timestamp','lex_polarity']).size()
        df = df.reset_index()

        df.columns = ['timestamp', 'polarity', 'size']

        dims = (20, 7)
        fig, ax = plt.subplots(figsize=dims)

        ax = sns.lineplot(ax=ax, x='timestamp', y='size', hue='polarity', palette='pastel', data=df)
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Tweets")

        fig.savefig(celebrity + ".pdf")