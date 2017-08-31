# -*- coding: utf-8 -*-
from auxiliar_functions import related_topics
import numpy as np
import datetime
import cPickle as pk
from sklearn.preprocessing import Normalizer

foldername = u'LaNacion_politica_feb_mar_abr'

n_topics = 152

norm2 = Normalizer('l2')

for topic in range(n_topics):

    vector = pk.load(file('{}/topic{}_vect.pk'.format(foldername, topic),\
                                                                  'r'))
    try:
        B[topic] = vector
    except:
        B = np.zeros([n_topics, len(vector)]) 
        B[topic] = vector

n_topics = B.shape[0]

B = norm2.fit_transform(B)

dissim = np.ones(n_topics, dtype = np.float) - B.dot(B.T)

from sklearn.cluster import AgglomerativeClustering as AC
from sklearn.metrics import silhouette_score as sil

data = []

for n in range(2, n_topics):
     ac = AC(n, affinity = 'precomputed', linkage = 'average')
     labels = ac.fit_predict(dissim)
     data.append(sil(dissim, labels, metric = 'precomputed'))
     print n, sil(dissim, labels, metric = 'precomputed')
"""
eps = 2 * np.std(np.diff(data))

for n in range(2, n_topics):
    if data[n-2] > np.max(data) - eps:
        break

print n
print np.argmax(np.array(data)) - 2

ac = AC(n, affinity = 'precomputed', linkage = 'average')
labels = ac.fit_predict(dissim)

topics_in_topics = {}
n_topics = set(labels)
for top in n_topics:
    topics_in_topics[top] = [i for i in range(len(labels)) \
                                 if labels[i] == top]

pk.dump(topics_in_topics, file('{}/Fusion_labels.pk'.format(foldername),'w'))
"""
