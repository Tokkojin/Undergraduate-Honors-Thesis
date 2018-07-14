import datetime
import pickle
import json
import pandas as pd

import nltk

from nltk.tokenize import TweetTokenizer
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import demo_liu_hu_lexicon as liu_hu_lexicon

from nltk.corpus import opinion_lexicon
from nltk.tokenize import treebank

from twitterscraper import query_tweets


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


if __name__ == '__main__':
    # Collecting the tweets
    # list_of_tweets = query_tweets(("James Franco"), limit=None, begindate=dt.date(2017, 6, 1), enddate=dt.date(2017, 6, 2),
    #                              poolsize=20, lang='en');

    # with open('james_franco.pkl', 'wb') as outfile:
    #    pickle.dump(list_of_tweets, outfile)

    # Opening from collection
    # with open('james_franco.pkl', 'rb') as infile:
    #     tweets = pickle.load(infile)
    #
    # tweets_serial = []
    # for tweet in tweets:
    #     tweets_serial.append(tweet.__dict__)
    #     print(tweet.__dict__)
    #
    # with open('james_franco.json', 'w') as outfile:
    #     json.dump(tweets_serial, outfile, default=datetime_handler)

    franco_corpus = pd.read_json('james_franco.json')
    franco_corpus['pol'] = 'neutral'

    tknz = TweetTokenizer()
    sa = SentimentAnalyzer()

    tokenizer = treebank.TreebankWordTokenizer()

    # might want to re-write this using apply()
    for index, row in franco_corpus.iterrows():
        pos_words = 0
        neg_words = 0
        tokenized_sent = [word.lower() for word in tokenizer.tokenize(row['text'])]

        for word in tokenized_sent:
            if word in opinion_lexicon.positive():
                pos_words += 1
            elif word in opinion_lexicon.negative():
                neg_words += 1

            # neutral words not counted

        if pos_words > neg_words:
            print('Positive')
            franco_corpus.loc[index, 'pol'] = 'positive'
        elif pos_words < neg_words:
            print('Negative')
            franco_corpus.loc[index, 'pol'] = 'negative'
        elif pos_words == neg_words:
            print('Neutral')
            franco_corpus.loc[index, 'pol'] = 'neutral'


    # not dealing with duplicates -- adding them to score
    # give a higher score for having been retweeted?

    # Pre-processing
    # Restore popular abbreviations to their corresponding original forms
    # TODO: Find lexicon of abbreviations.
    # External links and usernames (significanted by the @ sign) are eliminated
    # Punctuations are kept! (Sentiment can be expressed with emoticons)
    # Separate tweets into individual sentences
    # Tokenize an perform part of speech (POS) tagging for each sentence

    # Lexical-based method
