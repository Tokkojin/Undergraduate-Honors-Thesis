#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle
import pprint
import sys
import string
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Comment

# from sklearn.feature_extraction.text import CountVectorizer

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

if __name__ == '__main__':
    infile = sys.argv[1] + '.csv'

    df = pd.read_csv(infile)
    
    links = dict(zip(df.id, df.URL))
    
    # This uses the 3-argument version of str.maketrans
    # with arguments (x, y, z) where 'x' and 'y'
    # must be equal-length strings and characters in 'x'
    # are replaced by characters in 'y'. 'z'
    # is a string (string.punctuation here)
    # where each character in the string is mapped
    # to None
    translator = str.maketrans('', '', string.punctuation)
    pp = pprint.PrettyPrinter(indent=4)
    id_body_dict = {}
    
    for uid, link in links.items():
        link_clean = link.translate(translator)
        if(link_clean.find('youtube') == -1 and link_clean.find('twitter') == -1):
            try:
                html_page = urlopen(link)
                body = text_from_html(html_page)
                if(len(body) > 0):
                    id_body_dict[uid] = body
                    pp.pprint(id_body_dict)
            except HTTPError as e:
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
            except URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            else:
                print('?')
    
    outpickle = sys.argv[1] + '_linkbodytext.pkl'
    
    with open(outpickle, 'wb') as handle:
        pickle.dump(id_body_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

#    with open('filename.pickle', 'rb') as handle:
#        b = pickle.load(handle)
    
