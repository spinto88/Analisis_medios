# -*- coding: utf-8 -*-
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer as Tfidf
import cPickle as pk

conn = sqlite3.connect('data.db')

c = conn.cursor()

content = []
c.execute('select title, body from lanacion where title IS NOT NULL;')

for row in c:
    try:
        content.append(row[0] + row[1])
    except:
        content.append(row[0])

c.execute('select title, body from pagina12 where title IS NOT NULL;')

for row in c:
    try:
        content.append(row[0] + row[1])
    except:
        content.append(row[0])

conn.close()

"""
Entrenamiento de la valorizacion tfidf
"""
m = 0.00
while m <= 0.95:

    tfidf = Tfidf(min_df = m, max_df = m + 0.05, ngram_range = (1,2))
    x_tfidf = tfidf.fit_transform(content)
    print m, x_tfidf.shape[1]
    m += 0.05
