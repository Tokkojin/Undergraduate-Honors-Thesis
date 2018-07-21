import pandas as pd

from nltk.corpus import opinion_lexicon
from nltk.tokenize import treebank

import sys

from multiprocessing import cpu_count, Pool

from tqdm import tqdm

from datetime import datetime

tokenizer = treebank.TreebankWordTokenizer()

def get_lexicon_polarity(row):
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

    # print(row['text'] + ': ' + polarity)

    return polarity

def process_data(func, df, num_processes=None):
    if num_processes == None:
        num_processes = min(df.shape[0], cpu_count())

    with Pool(processes = num_processes) as pool:
        seq = []

        for index, row in df.iterrows():
            seq.append(row)

        results_list = list(tqdm(pool.imap(get_lexicon_polarity, seq), total=len(df.index)))

        df['lex_polarity'] = results_list

if __name__ == '__main__':
    infile = sys.argv[1] + '.json'
    outfile = sys.argv[1] + '_lex_pol.json'

    print('reading from ' + infile)

    corpus = pd.read_json(infile)

    # Enable to debug
    # corpus = corpus.head(10)
    corpus['lex_polarity'] = ''

    print('identifying sentiments...')

    # start = datetime.now()
    process_data(get_lexicon_polarity, corpus, num_processes=cpu_count())
    # print('time elapsed: ' + str(datetime.now() - start))

    #corpus['lexicon_polarity'] = pool.apply_async(corpus.apply,
     #                                             args=(get_lexicon_polarity, 'axis=1'))

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
