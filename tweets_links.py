import pandas as pd
from bs4 import BeautifulSoup

import sys

from multiprocessing import cpu_count, Pool

from tqdm import tqdm

import pickle


def find_URL(row):
    soup = BeautifulSoup(row['html'], 'html.parser')

    links = []

    for link in soup.find_all('a'):
        links.append(link)
        print(link.get('href'))

    return links

def process_data(func, df, num_processes=None):
    if num_processes == None:
        num_processes = min(df.shape[0], cpu_count())

    with Pool(processes = num_processes) as pool:
        rows = []

        for index, row in df.iterrows():
            rows.append(row)

        URLs = list(tqdm(pool.imap(find_URL, rows), total=len(df.index)))

    return URLs


if __name__ == '__main__':
    infile = sys.argv[1] + '.json'
    outfile = sys.argv[1] + '.pkl'

    print('reading from ' + infile)
    corpus = pd.read_json(infile)

    print('finding URLs...')
    URLs = process_data(find_URL, corpus, num_processes=cpu_count())

    print('saving to ' + outfile)

    with open(outfile, 'wb') as fp:
        pickle.dump(URLs, fp)

    # To load from .pkl...
    # with open('outfile', 'rb') as fp:
    #     itemlist = pickle.load(fp)