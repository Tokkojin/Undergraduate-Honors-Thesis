from datetime import datetime, date, timedelta

import json

import sys

from twitterscraper import query_tweets

def collect_tweets(name, articleDate):
    name = name.lower()

    articleDate = datetime.strptime(articleDate, '%m/%d/%y')
    beginDate = articleDate + timedelta(days=90)
    endDate = articleDate - timedelta(days=90)

    tweets = query_tweets(name, limit=None, begindate=beginDate, enddate=endDate,
                          poolsize=50, lang='en')

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
    # James Franco ~ January 11 2018
    # Dan Harmon ~ January ? 2018
    # Kevin Spacey ~ October 2017

    # TODO: May want to add more search terms.
    name = sys.argv[1]
    articleDate = sys.argv[2]

    print('Collecting tweets for ' + name)
    print('Article release ~ ' + articleDate + '\n')

    collect_tweets(name, articleDate)
