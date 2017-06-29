# -*- coding: utf-8 -*-
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer as Tfidf
import cPickle as pk
import numpy as np
import codecs

"""
Consulta a la base de datos
"""

newspaper = 'lanacion'
init_date = '2017-04-01'
final_date = '2017-05-01'
section = 'Política'

conn = sqlite3.connect('data.db')

c = conn.cursor()

c.execute('select title, body from {} where date >= "{}" and date <= "{}" and section == "{}" and title IS NOT NULL and body IS NOT NULL;'.format(newspaper, init_date, final_date, section))
content = [row[0] + row[1] for row in c]
conn.close()

"""
Analisis tf-idf y NMF de las notas
"""

tfidf = pk.load(open('Tfidf_transformer.pk','r'))
xtfidf = tfidf.transform(content)

shape = xtfidf.shape[0] * xtfidf.shape[1]
effective_shape = shape - list(xtfidf.getnnz(0)).count(0) * xtfidf.shape[0]
nnz = xtfidf.count_nonzero()
topics = int(np.ceil(np.float(effective_shape) / nnz))

print 'Cantidad de notas: {}'.format(len(content))
print 'Tópicos estimados: {}'.format(topics)

from sklearn.decomposition import NMF

nmf = NMF(n_components = topics, max_iter = 1000)
nmf_array = nmf.fit_transform(xtfidf)

argmaxs = [np.argmax(x) for x in nmf_array]
print sorted(argmaxs, reverse = True, key = lambda x: argmaxs.count(x))

components = nmf.components_
features = tfidf.vocabulary_.items()

j = 0
for comp in components:
    ordered_features = sorted(features, reverse = True, key = lambda x: comp[x[1]])
    features_name = [of[0] for of in ordered_features]

    fp = codecs.open('{}_{}_1month.txt'.format(newspaper, init_date), 'a', 'utf8')
    fp.write('{}, '.format(j))
    for fn in range(20):
        fp.write(u'{}, '.format(features_name[fn]))
    fp.write('\n')
    fp.close()

    j += 1
