import datetime as dt

import json

from twitterscraper import query_tweets


def datetime_handler(x):
    if isinstance(x, dt.datetime):
        return x.isoformat()
    raise TypeError('Unknown type')


if __name__ == '__main__':
    # Collecting the tweets
    # James Franco article came out on January 11 2018

    # TODO: Write collection process into a method that takes the celebrity's name and date
    # of when their article came out.
    # Additionally, may want to add more search terms.
    tweets = query_tweets('James Franco', limit=None, begindate=dt.date(2017, 9, 1), enddate=dt.date(2018, 3, 31),
                          poolsize=20, lang='en')

    tweets_serialized = [tweet.__dict__ for tweet in tweets]

    with open('james_franco.json', 'w') as outfile:
        json.dump(tweets_serialized, outfile, default=datetime_handler)
        print('tweets saved!')
