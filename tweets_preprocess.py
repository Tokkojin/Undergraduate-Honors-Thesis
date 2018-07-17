import pandas as pd
from tqdm import tqdm, tqdm_pandas

from nltk.tokenize import TweetTokenizer
from nltk.sentiment import SentimentAnalyzer
from nltk.corpus import opinion_lexicon, stopwords
from nltk.tokenize import treebank

tknz = TweetTokenizer()
sa = SentimentAnalyzer()

tokenizer = treebank.TreebankWordTokenizer()

# Create and register a new `tqdm` instance with `pandas`
# (can use tqdm_gui, optional kwargs, etc.)
tqdm_pandas(tqdm())

def get_lexicon_polarity(row):
    # Possible improvements: Make entity-based; consider lexicon in context
    polarity = ''
    pos_words = 0
    neg_words = 0

    tokenized_sent = [word.lower() for word in tokenizer.tokenize(row['text'])]

    for word in tokenized_sent:
        if word in opinion_lexicon.positive():
            pos_words += 1
        elif word in opinion_lexicon.negative():
            neg_words += 1

    if pos_words > neg_words:
        polarity = 'positive'
    elif pos_words < neg_words:
        polarity = 'negative'
    elif pos_words == neg_words:
        polarity = 'neutral'

    return polarity

if __name__ == '__main__':
    franco_corpus = pd.read_json('james_franco.json')

    franco_corpus['lexicon_polarity'] = franco_corpus.progress_apply(get_lexicon_polarity, axis=1)

    franco_corpus.to_json(path_or_buf='james_franco_lex_pol.json')


    # not dealing with duplicates -- adding them to score
    # give a higher score for having been retweeted?

    # Pre-processing
    # Restore popular abbreviations to their corresponding original forms
    # TODO: Find lexicon of abbreviations.
    # External links and usernames (signified by the @ sign) are eliminated
    # Punctuations are kept! (Sentiment can be expressed with emoticons)
    # Separate tweets into individual sentences
    # Tokenize an perform part of speech (POS) tagging for each sentence

    # Lexical-based method
