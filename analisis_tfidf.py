# -*- coding: utf-8 -*-

import auxiliar_functions as aux_func

newspaper = 'lanacion'
#section = u'Deportes'
section = None

foldername = 'LaNacion_marzo'

init_date = '2017-03-01'
final_date = '2017-04-01'

xtfidf, features, ids_relation, content = aux_func.tfidf_matrix(newspaper, \
                                            init_date, final_date, section) 

ntopics, features_filtered = aux_func.topics_estimation(xtfidf, \
                                           features, delta = 0.05)

print ntopics

xnmf, components = aux_func.nmf_decomposition(xtfidf, ntopics)

aux_func.save_features(foldername, features, components, nprincipal = 20)
aux_func.save_temporal_profile(foldername, xnmf, ids_relation, content)
