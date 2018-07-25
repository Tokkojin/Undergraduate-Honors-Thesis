#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import csv

import pandas as pd

def find_URL(row):
    URLs = re.findall(r'(https?://[^\s]+)', row['text'])
    
    for URL in URLs:
        csvwriter.writerows( [[str(row['timestamp']), URL, row['likes'], row['replies'], row['retweets']]] )

if __name__ == '__main__':
    infile = sys.argv[1] + '.json'
    outfile = sys.argv[1] + '.csv'

    with open(infile, 'rb') as fp:
        corpus = pd.read_json(infile)
    
    f = open(outfile, 'w', newline='')
    csvwriter = csv.writer(f)
    csvwriter.writerows( [['timestamp', 'URL', 'likes', 'replies', 'retweets']] )
    
    corpus.apply(find_URL, axis=1)
    
    f.close()
    