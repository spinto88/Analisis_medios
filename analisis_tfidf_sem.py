# -*- coding: utf-8 -*-

import auxiliar_functions as aux_func
import datetime

newspaper = 'lanacion'
section = u'Política'
#section = None

date = datetime.date(2017,1,2)

sem = 1
offset = 0
while date < datetime.date(2017,8,01):

    date2 = date + datetime.timedelta(7)

    foldername = 'LaNacion_sem{}'.format(sem)

    xtfidf, features, ids_relation, content = aux_func.tfidf_matrix(newspaper, \
                                            date, date2, section) 

    ntopics, features_filtered, \
             inferior, superior, density = aux_func.topics_estimation(xtfidf, \
                                 features, delta = 0.00)

    ntopics = 5

    xnmf, components = aux_func.nmf_decomposition(xtfidf, ntopics)

    aux_func.save_features(foldername, features, components, nprincipal = 20, offset = offset)
    aux_func.save_temporal_profile(foldername, xnmf, ids_relation, content, offset = offset)

    offset += ntopics
    sem += 1

    date += datetime.timedelta(7)
