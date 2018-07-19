import datetime as dt

import json

import sys

from twitterscraper import query_tweets

def collect_tweets(name):
    name = name.lower()

    tweets = query_tweets(name, limit=None, begindate=dt.date(2017, 9, 1), enddate=dt.date(2018, 3, 31),
                          poolsize=20, lang='en')

    tweets_serialized = [tweet.__dict__ for tweet in tweets]

    outfile_str = name.replace(' ', '_') + '.json'

    with open(outfile_str, 'w') as outfile:
        json.dump(tweets_serialized, outfile, default=datetime_handler)
        print('tweets saved!')

def datetime_handler(x):
    if isinstance(x, dt.datetime):
        return x.isoformat()
    raise TypeError('Unknown type')

if __name__ == '__main__':
    # Collecting the tweets
    # James Franco article came out on January 11 2018
    # Dan Harmon article(?) came out January ? 2018

    # TODO: May want to add more search terms.
    name = sys.argv[1]
    print('Collecting tweets for ' + name)
    collect_tweets(name)
