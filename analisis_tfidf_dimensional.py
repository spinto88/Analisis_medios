# -*- coding: utf-8 -*-
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer as Tfidf
from sklearn.decomposition import NMF
import cPickle as pk
import numpy as np
import codecs
import csv
import os
import datetime
from copy import deepcopy
from sklearn.preprocessing import Normalizer
import matplotlib.pyplot as plt

"""
Database query
"""
newspaper = 'lanacion'
init_date = '2017-03-01'
final_date = '2017-06-01'
section = u'Política'

tfidf = pk.load(open('Tfidf_all.pk', 'r'))

conn = sqlite3.connect('data.db')
c = conn.cursor()

ids_relation = []
content = []
c.execute(u'select id, date, title, body from {} where date >= "{}" and date <= "{}" and section == "{}" and title IS NOT NULL;'.format(newspaper, init_date, final_date, section))
for row in c:
    try:
        content.append(row[2] + row[3])
    except:
        content.append(row[2])

    ids_relation.append({'db_id': row[0], \
        'date': datetime.datetime.strptime(row[1], "%Y-%m-%d").date()})

conn.close()

"""
Tf-idf transform
"""
features = tfidf.vocabulary_.items()
xtfidf = tfidf.transform(content)

"""
Topic estimation
"""
#shape = xtfidf.shape[0] * xtfidf.shape[1]
print xtfidf.shape

"""
Histogram of nonzero columns
"""
"""
plt.figure(1)
hist = np.bincount(xtfidf.getnnz(0))
plt.plot(hist, '.-')
plt.grid('on')
plt.xscale('symlog')
plt.yscale('symlog')

plt.figure(2)
plt.plot([i * hist[i] for i in range(len(hist))], '.-')
plt.grid('on')
plt.xscale('symlog')
plt.yscale('symlog')
"""

hist = np.bincount(xtfidf.getnnz(0))
non_zero = [i * hist[i] for i in range(len(hist))]
non_zero = np.array(non_zero, dtype = np.float)/np.sum(non_zero)
"""
plt.figure(3)
plt.plot(non_zero, '.-')
plt.grid('on')
plt.xscale('symlog')
#plt.yscale('symlog')
"""

plt.figure(4)
plt.plot([np.sum(non_zero[:i+1]) for i in range(len(non_zero))], '.-')
#plt.plot([np.sum(non_zero[-i-1:]) for i in range(len(non_zero))], '.-')
plt.grid('on')
plt.xscale('symlog')
#plt.yscale('symlog')

cum_non_zero = [np.sum(non_zero[:i+1]) for i in range(len(non_zero))]

j = sorted(range(len(cum_non_zero)), key = lambda x: np.abs(cum_non_zero[x] - 0.5))[0]

print np.ceil((xtfidf.shape[0] * cum_non_zero[j])/j)

plt.show()
"""
nnz = xtfidf.count_nonzero()
topics = int(np.ceil(np.float(effective_shape) / nnz))
print 'Cantidad de notas: {}'.format(len(content))
print 'Tópicos estimados: {}'.format(topics)
"""

