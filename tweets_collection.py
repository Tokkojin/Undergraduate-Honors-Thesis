from datetime import datetime, date, timedelta

import json

import sys

from twitterscraper import query

def collect_tweets(name, articleDate):
    name = name.lower()

    articleDate = datetime.strptime(articleDate, '%m/%d/%y')
    beginDate = (articleDate - timedelta(days=90)).date()
    endDate = (articleDate + timedelta(days=90)).date()

    # Collect tweets with mentions in the form of "FirstName LastName"
    tweets = query.query_tweets(name, limit=None, begindate=beginDate, enddate=endDate, poolsize=40, lang='en')
    tweets_serialized_pt1 = [tweet.__dict__ for tweet in tweets]

    # Collect tweets with mentions in the form of "FirstNameLastName"
    no_space_name = name.replace(' ', '')

    tweets = query.query_tweets(no_space_name, limit=None, begindate=beginDate, enddate=endDate, poolsize=40, lang='en')
    tweets_serialized_pt2 = [tweet.__dict__ for tweet in tweets]

    tweets_serialized = tweets_serialized_pt1 + tweets_serialized_pt2

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
    name = input("Name (FirstName LastName): ")
    articleDate = input("Article date (mm/dd/yy): ")

    print('Collecting tweets for ' + name)
    print('Article release ~ ' + articleDate + '\n')

    collect_tweets(name, articleDate)
