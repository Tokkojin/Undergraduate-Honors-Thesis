#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import string
import sys

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize

from sklearn.cluster import KMeans
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd

def clean_text(text):
    tokens = word_tokenize(text)
    stemmer = SnowballStemmer("english")
    
    tokens = [w.lower() for w in tokens]    
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    stems = [stemmer.stem(t) for t in words]
    
    return stems

if __name__ == '__main__':
    infile = sys.argv[1] + '_linkbodytext.json'
    
    link_text = pd.read_json(infile)
    link_text = link_text.dropna()
    
    link_text = pd.DataFrame(link_text[0].values.tolist())
    link_text.columns = ['uid', 'link', 'body_text']
    link_text['body_text'] = link_text['body_text'].str.strip()
    link_text = link_text.drop(link_text[link_text.body_text == ''].index)
    
    link_text['words'] = link_text['body_text'].map(clean_text)
    corpus = link_text['body_text'].tolist()
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    terms = vectorizer.get_feature_names()
    
    num_clusters = 5
    
    km = KMeans(n_clusters=num_clusters)
    
    km.fit(tfidf_matrix)
    
    clusters = km.labels_.tolist()
    link_text['clusters'] = clusters
    .value_counts()
    
    joblib.dump(km,  'doc_cluster.pkl')
    
    #km = joblib.load('doc_cluster.pkl')
    clusters = km.labels_.tolist()