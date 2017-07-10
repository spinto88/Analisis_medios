# -*- coding: utf-8 -*-
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer as Tfidf
import cPickle as pk

init_date = "2017-03-01"
final_date = "2017-03-01"
lanacion_section = u'Política'
pagina12_equivalence = {u'Política': u'El país'}

conn = sqlite3.connect('data.db')
c = conn.cursor()

c.execute(u'select title, body from lanacion where title IS NOT NULL and body IS NOT NULL and section == "{}" and date >= "{}" and date <= "{}";'.format(lanacion_section, init_date, final_date))
content = [row[0] + row[1] for row in c]

c.execute(u'select title, body from pagina12 where title IS NOT NULL and body IS NOT NULL and section == "{}" and date >= "{}" and date <= "{}";'.format(pagina12_equivalence[lanacion_section], init_date, final_date))
content += [row[0] + row[1] for row in c]

conn.close()

# Entrenamiento de la valorizacion tfidf

tfidf = Tfidf(min_df = 0.01, max_df = 0.5, ngram_range = (1,3))
tfidf.fit(content)

pk.dump(tfidf, open('Tfidf_section{}_id{}_fd{}.pk'.format(lanacion_section[0], init_date, final_date),'w'))

