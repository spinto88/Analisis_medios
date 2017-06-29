# -*- coding: utf-8 -*-
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer as Tfidf
import cPickle as pk

conn = sqlite3.connect('data.db')

c = conn.cursor()

c.execute('select title, body from lanacion where title IS NOT NULL and body IS NOT NULL;')
content = [row[0] + row[1] for row in c]
c.execute('select title, body from pagina12 where title IS NOT NULL and body IS NOT NULL;')
content += [row[0] + row[1] for row in c]

conn.close()

"""
Entrenamiento de la valorizacion tfidf
"""

tfidf = Tfidf(min_df = 0.005, max_df = 0.10, ngram_range = (1,2))
tfidf.fit(content)

pk.dump(tfidf, open('Tfidf_transformer.pk','w'))


