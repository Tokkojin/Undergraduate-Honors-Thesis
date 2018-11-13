import pandas as pd
import sys
from multiprocessing import cpu_count, Pool
from tqdm import tqdm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def vader_sentiment(txt):
    vs = analyzer.polarity_scores(txt)

    score = vs['compound']

    if score < -0.05:
        return 'negative'
    elif score > 0.05:
        return 'positive'
    else:
        return 'neutral'

def process_data(func, df, num_processes=None):
    if num_processes == None:
        num_processes = min(df.shape[0], cpu_count())

    with Pool(processes = num_processes) as pool:
        seq = df['text'].tolist()

        results_list = list(tqdm(pool.imap(func, seq), total=len(df.index)))

        df['lex_polarity'] = results_list

if __name__ == '__main__':
    infile = sys.argv[1] + '.json'
    outfile = sys.argv[1] + '_lex_pol.json'

    print('reading from ' + infile)

    corpus = pd.read_json(infile)

    print('identifying sentiments...')
    process_data(vader_sentiment, corpus, num_processes=cpu_count())

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