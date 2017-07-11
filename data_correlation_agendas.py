# -*- coding: utf-8 -*-
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer as Tfidf
from sklearn.decomposition import NMF
import cPickle as pk
import datetime
from copy import deepcopy
from sklearn.preprocessing import Normalizer
import numpy as np
import os
import codecs

init_date = datetime.date(2017, 3, 1)
final_date = datetime.date(2017, 6, 1)
date = deepcopy(init_date)

lanacion_section = u'Política'
pagina12_equivalence = {u'Política': u'El país'}
  
conn = sqlite3.connect('data.db')
c = conn.cursor()

newspaper = 'lanacion'

largo_del_periodo = 7

while date < final_date:

    c.execute(u'select title, body from lanacion where title IS NOT NULL and body IS NOT NULL and section == "{}" and date >= "{}" and date < "{}";'.format(lanacion_section, str(date), str(date + datetime.timedelta(largo_del_periodo))))
    content = [row[0] + row[1] for row in c]

    c.execute(u'select title, body from pagina12 where title IS NOT NULL and body IS NOT NULL and section == "{}" and date >= "{}" and date < "{}";'.format(pagina12_equivalence[lanacion_section], str(date), str(date + datetime.timedelta(largo_del_periodo))))
    content += [row[0] + row[1] for row in c]

    # Entrenamiento de la valorizacion tfidf
    tfidf = Tfidf(min_df = 0.01, max_df = 0.50, ngram_range = (1,3))
    tfidf.fit(content)

    # Ajuste tfidf
    ids_relation = []
    content = []
    c.execute(u'select id, date, title, body from {} where date >= "{}" and date < "{}" and section == "{}" and title IS NOT NULL;'.format(newspaper, str(date), str(date + datetime.timedelta(largo_del_periodo)), (lambda x: lanacion_section if x == 'lanacion' else pagina12_equivalence[lanacion_section])(newspaper)))
    for row in c:
        try:
            content.append(row[2] + row[3])
        except:
            content.append(row[2])

    ids_relation.append({'db_id': row[0], \
        'date': datetime.datetime.strptime(row[1], "%Y-%m-%d").date()})

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
    ntopics = int(np.ceil(np.float(effective_shape) / nnz))

    """
    NMF decomposition
    """
    nmf = NMF(n_components = ntopics, max_iter = 1000)
    nmf_array = nmf.fit_transform(xtfidf)
    components = list(nmf.components_)
    notes_topics = [np.argmax(x) for x in nmf_array]

    """
    Normalize nmf vectors to norm 1
    """
    norm1 = Normalizer(norm = 'l1')
    nmf_array = norm1.fit_transform(nmf_array)

    topics_weight = []

    for comp_j in range(nmf_array.shape[1]):
        topic_weight = 0.00
        for i in range(nmf_array.shape[0]):
            topic_weight += len(content[i]) * nmf_array[i][comp_j]
        topics_weight.append(topic_weight)

    ordered_topics = sorted(range(nmf_array.shape[1]), key = lambda x: topics_weight[x], reverse = True)
    
    foldername = '{}_week{}/'.format(newspaper, date)
    os.mkdir(foldername)
    for comp_index in ordered_topics[:5]:

        """ Intepretation """
        ordered_features = sorted(features, reverse = True, key = lambda x: tfidf.idf_[x[1]] * components[comp_index][x[1]])
        features_name = [of[0] for of in ordered_features]

        fp = codecs.open(foldername + '{}_topics.txt'.format(newspaper), 'a', 'utf8')
        fp.write(u'Topic {}:\n'.format(comp_index))
        for fn in range(50):
            fp.write(u'{}, '.format(features_name[fn]))
        fp.write('\n')
        fp.close()

        """ Vector representation """
        pk.dump(components[comp_index], \
          file(foldername + '{}_topic{}_vect.pk'.format(newspaper, comp_index),'w'))


    date += datetime.timedelta(largo_del_periodo)


conn.close()
