#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import string
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

import pandas as pd
from bs4 import BeautifulSoup

if __name__ == '__main__':
    infile = sys.argv[1] + '.csv'

    df = pd.read_csv(infile)
    
    links = dict(zip(df.id, df.URL))
    
    for link in links.values():
        link = link.translate(None, string.punctuation)
        if(link.find('youtube') == -1):
            try:
                html_page = urlopen(link)
                soup = BeautifulSoup(html_page)
                body = soup.find_all("p")
                if(len(body) > 0):
                    print(body)
            except HTTPError as e:
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
            except URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            else:
                print('?')
    
