import datetime as dt
import pickle

from twitterscraper import query_tweets


if __name__ == '__main__':
    #list_of_tweets = query_tweets(("James Franco"), limit=None, begindate=dt.date(2017, 6, 1), enddate=dt.date(2017, 6, 2),
    #                              poolsize=20, lang='en');


    #with open('james_franco.pkl', 'wb') as outfile:
    #    pickle.dump(list_of_tweets, outfile)

    with open('james_franco.pkl', 'rb') as infile:
        tweets = pickle.load(infile)

    for tweet in tweets:
        print(tweet.retweets + tweet.text)

    # TODO: Sentiment analysis.
