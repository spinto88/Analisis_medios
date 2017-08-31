# -*- coding: utf-8 -*-

import auxiliar_functions as aux_func

newspaper = 'lanacion'
#section = u'El país'
section = None

foldername = 'LaNacion_feb_mar_abr'

init_date = '2017-02-01'
final_date = '2017-05-01'

xtfidf, features, ids_relation, content = aux_func.tfidf_matrix(newspaper, \
                                            init_date, final_date, section) 

ntopics, features_filtered, \
             inferior, superior, density = aux_func.topics_estimation(xtfidf, \
                                 features, delta = 0.05)

xnmf, components = aux_func.nmf_decomposition(xtfidf, ntopics)

aux_func.save_features(foldername, features, components, nprincipal = 20)
aux_func.save_temporal_profile(foldername, xnmf, ids_relation, content)
