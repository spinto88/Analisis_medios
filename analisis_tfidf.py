# -*- coding: utf-8 -*-

import auxiliar_functions as aux_func

newspaper = 'lanacion'
#section = u'Política'
section = None

init_date = '2017-03-01'
final_date = '2017-04-01'

xtfidf, features, ids_relation, content = aux_func.tfidf_matrix(newspaper, \
                                            init_date, final_date, section) 

ntopics, features_filtered = aux_func.topics_estimation(xtfidf, \
                                           features, delta = 0.05)

print ntopics

xnmf, components = aux_func.nmf_decomposition(xtfidf, ntopics)

x_temp = aux_func.temporal_profile(xnmf, ids_relation, content)

print x_temp.shape

import matplotlib.pyplot as plt
import numpy as np
plt.imshow(x_temp, cmap = 'bone_r', \
           interpolation = 'nearest', \
           vmin = 0, vmax = np.max(x_temp), \
           aspect = 'auto')
plt.show()

"""
pf = aux_func.principal_features(features_filtered, components)

for comp in pf:
    for feat in comp:
        print feat,
    print 
"""   



