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

"""
Where to save the results
"""
foldername = 'Data01-03_01-06/'
try:
    os.mkdir(foldername)
except:
    pass

"""
Database query
"""
newspaper = 'lanacion'
init_date = '2017-03-01'
final_date = '2017-06-01'
section = u'Política'
tfidf_id = 'P'

tfidf = pk.load(open('Tfidf_section{}_id{}_fd{}.pk'.format(tfidf_id, init_date, final_date),'r'))

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
shape = xtfidf.shape[0] * xtfidf.shape[1]
effective_shape = shape - list(xtfidf.getnnz(0)).count(0) * xtfidf.shape[0]
nnz = xtfidf.count_nonzero()
topics = int(np.ceil(np.float(effective_shape) / nnz))
print 'Cantidad de notas: {}'.format(len(content))
print 'Tópicos estimados: {}'.format(topics)

"""
NMF decomposition
"""
nmf = NMF(n_components = topics, max_iter = 1000)
nmf_array = nmf.fit_transform(xtfidf)
components = nmf.components_
notes_topics = [np.argmax(x) for x in nmf_array]

"""
Normalize components to norm 2
"""
norm2 = Normalizer(norm = 'l2')
components = norm2.fit_transform(components)

"""
Normalize nmf vectors to norm 1
"""
norm1 = Normalizer(norm = 'l1')
nmf_array = norm1.fit_transform(nmf_array)

"""
Interpretation and temporal profile
"""
j = 0
init_date = datetime.datetime.strptime(init_date, "%Y-%m-%d").date()
final_date = datetime.datetime.strptime(final_date, "%Y-%m-%d").date()
for comp in components:

    """ Intepretation """
    ordered_features = sorted(features, reverse = True, key = lambda x: tfidf.idf_[x[1]] * comp[x[1]])
    features_name = [of[0] for of in ordered_features]
    fp = codecs.open(foldername + '{}_topics.txt'.format(newspaper), 'a', 'utf8')
    fp.write(u'Topic {}:\n'.format(j))
    for fn in range(50):
        fp.write(u'{}, '.format(features_name[fn]))
    fp.write('\n')
    fp.close()

    """ Temporal profile """
    date = deepcopy(init_date)
    with open(foldername + '{}_topic{}_temp.csv'.format(newspaper, j), 'a') as csvfile:
        csvfile.write('date,topic_weight\n')
        while date <= final_date:
            topic_weight = 0.00
            for i in range(nmf_array.shape[0]):
                if ids_relation[i]['date'] == date:
                    topic_weight += len(content[i]) * nmf_array[i][j]
            csvfile.write('{},{}\n'.format(date, topic_weight))
            date += datetime.timedelta(1)
        csvfile.close()

    """ Vector representation """
    pk.dump(comp, file(foldername + '{}_topic{}_vect.pk'.format(newspaper, j),'w'))

    """ Notes asociated """
    with open(foldername + '{}_topic{}_notes.csv'.format(newspaper, j), 'a') as csvfile:
        csvfile.write('Database_ids_notes\n')
        for i in range(nmf_array.shape[0]):
            if notes_topics[i] == j:
                csvfile.write('{},'.format(ids_relation[i]['db_id']))
        csvfile.close()
    
    j += 1
