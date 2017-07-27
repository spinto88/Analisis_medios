# -*- coding: utf-8 -*-

def tfidf_matrix(newspaper, init_date, final_date, section):

    import sqlite3
    from sklearn.feature_extraction.text import TfidfVectorizer as Tfidf
    import cPickle as pk
    import datetime

    tfidf = pk.load(open('idf.pk', 'r'))

    order = u'select id, date, title, body from {}'.format(newspaper)
    if section != None:
        order += u' where section == "{}"'.format(section)
        order +=  u' and date >= "{}" and date < "{}" and title IS NOT NULL;'.format(init_date, final_date)
    else:
        order +=  u' where date >= "{}" and date < "{}" and title IS NOT NULL;'.format(init_date, final_date)

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(order)

    ids_relation = []
    content = []

    for row in c:
        try:
            content.append(row[2] + row[3])
        except:
            content.append(row[2])

        ids_relation.append({'db_id': row[0], \
            'date': datetime.datetime.strptime(row[1], "%Y-%m-%d").date()})

    conn.close()

    features = tfidf.vocabulary_.items()
    xtfidf = tfidf.transform(content)

    return xtfidf, features, ids_relation, content

def topics_estimation(xtfidf, features, delta = 0.20):

    import numpy as np

    N = xtfidf.shape[0]
    M = xtfidf.shape[1]
    nnz = list(xtfidf.getnnz(0))
    binc = np.bincount(nnz)

    density = [i * binc[i] for i in range(len(binc))]
    distribution = [np.sum(density[:i+1]) for i in range(len(density))]
    distribution = np.array(distribution, dtype = np.float)/np.max(distribution)

    inferior = min(range(len(distribution)), \
               key = lambda x: np.abs(distribution[x]-delta))

    superior = min(range(len(distribution)), \
               key = lambda x: np.abs(distribution[x]-1.00+delta))

    mp = M
    nnzp = np.sum(nnz)

    bcnnz = np.bincount(nnz)

    mp -= np.sum(binc[:inferior])
    nnzp -= np.sum([j * binc[j] for j in range(inferior)])
    mp -= np.sum(binc[superior:])
    nnzp -= np.sum([j * binc[j] for j in range(superior, len(distribution))])

    ntopics = int(N*mp/nnzp)

    features_filtered = filter(lambda x: nnz[x[1]] > inferior and \
                           nnz[x[1]] < superior, features)

    return ntopics, features_filtered 

def nmf_decomposition(xtfidf, ntopics, random_seed = 123457):

    from sklearn.decomposition import NMF

    nmf = NMF(ntopics, random_state = random_seed)

    xnmf = nmf.fit_transform(xtfidf)

    return xnmf, nmf.components_

def principal_features(features, components, nprincipal = 10):

    pf = []
    for comp in components:

        pf_per_comp = sorted(features, reverse = True, key = lambda x: comp[x[1]])[:nprincipal]

        pf.append([x[0] for x in pf_per_comp])

    return pf

def temporal_profile(xnmf, ids_relation, content):

    from sklearn.preprocessing import Normalizer
    import datetime
    import numpy as np
    
    norm1 = Normalizer('l1')

    xnmf = norm1.fit_transform(xnmf)

    ntopics = xnmf.shape[1]
    dates = sorted(list(set([idsr['date'] for idsr in ids_relation])))

    x_temp = np.zeros([ntopics, len(dates)], dtype = np.float)

    for i in range(xnmf.shape[0]):
        x_topic = np.argmax(xnmf[i])
        date_id = dates.index(ids_relation[i]['date'])
        x_temp[x_topic][date_id] += len(content[i]) * xnmf[i][x_topic]

    return x_temp
