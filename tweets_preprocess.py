import pandas as pd

from nltk.corpus import opinion_lexicon
from nltk.tokenize import treebank

import sys

from multiprocessing import cpu_count, Pool

from tqdm import tqdm

tokenizer = treebank.TreebankWordTokenizer()


def get_lexicon_polarity(corpus, index, row):
    # Possible improvements: Make entity-based; consider lexicon in context
    polarity = 'NaN'
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

    corpus.at[index,'lex_polarity'] = polarity


if __name__ == '__main__':
    infile = sys.argv[1] + '.json'
    outfile = sys.argv[1] + '_lex_pol.json'

    print('reading from ' + infile)

    corpus = pd.read_json(infile)
    corpus['lex_polarity'] = ''

    pool = Pool(cpu_count())

    print('identifying sentiments...')

    # pool.map(get_lexicon_polarity, corpus.iterrows())

    for index, row in tqdm(corpus.iterrows()):
        pool.apply_async(get_lexicon_polarity, args=(corpus, index, row))

    pool.close()
    pool.join()

    # corpus['lexicon_polarity'] = corpus.progress_apply(get_lexicon_polarity, axis=1)

    print('saving to ' + outfile)

    corpus.to_json(path_or_buf=outfile)

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
