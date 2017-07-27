# -*- coding: utf-8 -*-

import auxiliar_functions as aux_func

newspaper = 'lanacion'
#section = u'Deportes'
section = None

init_date = '2017-03-01'
final_date = '2017-04-01'

xtfidf, features, ids_relation, content = aux_func.tfidf_matrix(newspaper, \
                                            init_date, final_date, section) 

ntopics, features_filtered = aux_func.topics_estimation(xtfidf, \
                                           features, delta = 0.10)

print ntopics

xnmf, components = aux_func.nmf_decomposition(xtfidf, ntopics)

pf = aux_func.principal_features(features_filtered, components)

for comp in pf:
    for feat in comp:
        print feat,
    print 
   



