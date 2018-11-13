#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import string
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from tqdm import tqdm

import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Comment

from multiprocessing import cpu_count, Pool

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def page_scrape(tuple):
    uid, link = tuple

    link_clean = link.translate(translator)

    if (link_clean.find('youtube') == -1 and link_clean.find('twitter') == -1
            and link_clean.find('facebook') == -1):
        try:
            html_page = urlopen(link)
            body = text_from_html(html_page)
            if (len(body) > 0):
                return (uid, link, body)
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        except:
            print("Unexpected error:", sys.exc_info()[0])

if __name__ == '__main__':
    infile = sys.argv[1] + '.pkl'
    outfile = sys.argv[1] + '_linkbodytext.json'

    df = pd.read_pickle(infile)
    df = df.drop_duplicates()

    links = dict(zip(df.id, df.url))
    
    # This uses the 3-argument version of str.maketrans
    # with arguments (x, y, z) where 'x' and 'y'
    # must be equal-length strings and characters in 'x'
    # are replaced by characters in 'y'. 'z'
    # is a string (string.punctuation here)
    # where each character in the string is mapped
    # to None
    translator = str.maketrans('', '', string.punctuation)

    with Pool(processes = cpu_count()) as pool:
        results = list(tqdm(pool.imap(page_scrape, links.items()), total=len(links.items())))
    
    with open(outfile, 'w') as fp:
        json.dump(results, fp)
    
