import datetime as dt

from datetime import datetime, date, timedelta

import json

import sys

from twitterscraper import query

def collect_tweets(name, articleDate, delta=30):
    name = name.lower()

    articleDate = datetime.strptime(articleDate, '%m/%d/%y')
    beginDate = (articleDate - timedelta(days=delta)).date()
    endDate = (articleDate + timedelta(days=delta)).date()

    # Collect tweets with mentions in the form of "FirstName LastName"
    tweets = query.query_tweets(name, limit=None, begindate=beginDate, enddate=endDate, poolsize=5, lang='en')
    tweets_serialized_pt1 = [tweet.__dict__ for tweet in tweets]

    # Collect tweets with mentions in the form of "FirstNameLastName"
    no_space_name = name.replace(' ', '')
    underline_name = name.replace(' ', '_')

    tweets = query.query_tweets(no_space_name, limit=None, begindate=beginDate, enddate=endDate, poolsize=5, lang='en')
    tweets_serialized_pt2 = [tweet.__dict__ for tweet in tweets]

    tweets_serialized = tweets_serialized_pt1 + tweets_serialized_pt2

    print(tweets_serialized_pt1)

    outfile_str = underline_name + '_tweets' + '.json'

    with open(outfile_str, 'w') as outfile:
        json.dump(tweets_serialized, outfile, default=datetime_handler)
        print('tweets saved!')


def datetime_handler(x):
    if isinstance(x, dt.datetime):
        return x.isoformat()
    raise TypeError('Unknown type')


if __name__ == '__main__':
    # TODO: May want to add more search terms.
    name = input("Name (FirstName LastName): ")
    articleDate = input("Article date (mm/dd/yy): ")
    days = input("Number of days before/after to look at: ")

    print('Collecting tweets for ' + name)
    print('Article release ~ ' + articleDate + '\n')
    if not days:
        print("Looking at tweets 30 days before and after article release")
        collect_tweets(name, articleDate)    
    else: 
        print("Looking at tweets " + str(days) + " days before and after article release")
        collect_tweets(name, articleDate, int(days))
