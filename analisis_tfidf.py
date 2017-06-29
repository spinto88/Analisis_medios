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
foldername = 'Data/'
try:
    os.mkdir(foldername)
except:
    pass

"""
Database query
"""
newspaper = 'lanacion'
init_date = '2017-04-01'
final_date = '2017-04-10'
section = 'Política'

conn = sqlite3.connect('data.db')
c = conn.cursor()

ids_relation = []
content = []
c.execute('select id, date, title, body from {} where date >= "{}" and date <= "{}" and section == "{}" and title IS NOT NULL;'.format(newspaper, init_date, final_date, section))
for row in c:
    try:
        content.append(row[2] + row[3])
    except:
        content.append(row[2])

    ids_relation.append({'db_id': row[0], \
        'date': datetime.datetime.strptime(row[1], "%Y-%m-%d").date()})

conn.close()

"""
Tf-idf loading and transform
"""
tfidf = pk.load(open('Tfidf_transformer.pk','r'))
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
date = deepcopy(init_date)
for comp in components:

    """ Intepretation """
    ordered_features = sorted(features, reverse = True, key = lambda x: comp[x[1]])
    features_name = [of[0] for of in ordered_features]
    fp = codecs.open(foldername + '{}_topic{}.txt'.format(newspaper, j), 'a', 'utf8')
    for fn in range(50):
        fp.write(u'{}, '.format(features_name[fn]))
    fp.write('\n')
    fp.close()

    """ Temporal profile """
    with open(foldername + '{}_topic{}_temp.csv'.format(newspaper, j), 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter= ',')
        while date <= final_date:
            topic_weight = 0.00
            for i in range(nmf_array.shape[0]):
                if ids_relation[i]['date'] == date:
                    topic_weight += len(content[i]) * nmf_array[i][j]
            writer.writerow([date, topic_weight])
            date += datetime.timedelta(1)

    """ Vector representation """
    pk.dump(comp, file(foldername + '{}_topic{}_vect.pk'.format(newspaper, j),'w'))

    """ Notes asociated """
    with open(foldername + '{}_topic{}_notes.csv'.format(newspaper, j), 'a') as csvfile:
        fieldnames = ['database_ids']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for i in range(nmf_array.shape[0]):
            if notes_topics[i] == j:
                writer.writerow({'database_ids': ids_relation[i]['db_id']})
    
    j += 1
