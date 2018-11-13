#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import csv

import pandas as pd

def find_URL(row):
    URLs = re.findall(r'(https?://[^\s]+)', row['text'])
    
    if len(URLs) == 1:
        csvwriter.writerows( [[str(row['id']), str(row['timestamp']), URLs[0], row['likes'], row['replies'], row['retweets']]] )
    elif len(URLs) == 2 and URLs[0] == URLs[1]:
        csvwriter.writerows( [[str(row['id']), str(row['timestamp']), URLs[0], row['likes'], row['replies'], row['retweets']]] )        
    else:
        count = 0
        for URL in URLs:
            new_id = str(row['id']) + '_' + str(count)
            csvwriter.writerows( [[ new_id, str(row['timestamp']), URL, row['likes'], row['replies'], row['retweets'] ]] )
            count += 1

if __name__ == '__main__':
    infile = sys.argv[1] + '.pkl'
    outfile = sys.argv[1] + '_links.csv'

    with open(infile, 'rb') as fp:
        corpus = pd.read_pickle(infile)

    f = open(outfile, 'w', newline='')
    csvwriter = csv.writer(f)
    csvwriter.writerows( [['id', 'timestamp', 'URL', 'likes', 'replies', 'retweets']] )

    corpus.apply(find_URL, axis=1)
    
    f.close()
    