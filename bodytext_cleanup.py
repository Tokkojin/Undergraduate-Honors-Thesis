#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import pandas as pd

if __name__ == '__main__':
    infile = sys.argv[1] + '_linkbodytext.json'
    
    link_text = pd.read_json(infile)
    link_text = link_text.dropna()
    
    link_text = pd.DataFrame(link_text[0].values.tolist())
    link_text.columns = ['uid', 'link', 'body_text']
    link_text['body_text'] = link_text['body_text'].str.strip()
    link_text = link_text.drop(link_text[link_text.body_text == ''].index)