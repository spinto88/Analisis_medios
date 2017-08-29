# -*- coding: utf-8 -*-
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer as Tfidf
import cPickle as pk

init_date = "2017-01-01"
final_date = "2017-08-01"
#lanacion_section = u'Política'
#pagina12_equivalence = {u'Política': u'El país'}

conn = sqlite3.connect('data.db')
c = conn.cursor()

c.execute(u'select title, body from lanacion where title IS NOT NULL and body IS NOT NULL and date >= "{}" and date <= "{}";'.format(init_date, final_date))
content = [row[0] + row[1] for row in c]

c.execute(u'select title, body from pagina12 where title IS NOT NULL and body IS NOT NULL and date >= "{}" and date <= "{}";'.format(init_date, final_date))
content += [row[0] + row[1] for row in c]

conn.close()

"""
Palabras comunes
"""
import codecs
fp = codecs.open("stopwords.txt", "r", encoding = "utf-8")
data = fp.read()
fp.close()
words = data.split('\r\n')

# Entrenamiento de la valorizacion tfidf

tfidf = Tfidf(min_df = 2, max_df = 0.95, \
              stop_words = words, \
              ngram_range = (1,1))

tfidf.fit(content)

pk.dump(tfidf, open('idf.pk','w'))

