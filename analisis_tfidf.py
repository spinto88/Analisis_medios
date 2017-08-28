# -*- coding: utf-8 -*-

import auxiliar_functions as aux_func

newspaper = 'pagina12'
section = u'El país'
#section = None

foldername = 'Pagina12_politica_4meses'

init_date = '2017-03-01'
final_date = '2017-06-01'

xtfidf, features, ids_relation, content = aux_func.tfidf_matrix(newspaper, \
                                            init_date, final_date, section) 

ntopics, features_filtered, \
             inferior, superior, density = aux_func.topics_estimation(xtfidf, \
                                 features, delta = 0.10)

#print xtfidf.shape
print ntopics, inferior, superior

import matplotlib.pyplot as plt

plt.axes([0.2, 0.2, 0.70, 0.70])
plt.hist(range(len(density)), weights = density, bins = 20, log = True, normed = True)
plt.ylabel('Densidad de columnas', size = 15)
plt.xticks(size = 15)
plt.yticks(size = 15)
plt.xlabel('Cantidad de elementos no nulos', size = 15)
plt.savefig('histograma_de_elementos_no_nulos.eps')
plt.show()

exit()

xnmf, components = aux_func.nmf_decomposition(xtfidf, ntopics)

aux_func.save_features(foldername, features, components, nprincipal = 20)
aux_func.save_temporal_profile(foldername, xnmf, ids_relation, content)
