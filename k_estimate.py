#! -*- coding: utf-8 -*-

# Estimación de la cantidad de tópicos a partir de su 
# comparación con un método de clustering aglomerativo

def nmf_array_seed(data, k = 2, seed = 1234578):

    from sklearn.decomposition import NMF
    import numpy as np
    from sklearn.preprocessing import Normalizer

    documents = data.shape[0]
    features = data.shape[1]

    norm2 = Normalizer('l2')
    data = norm2.fit_transform(data)

    nmf = NMF(k, random_state = seed)

    nmf_array = nmf.fit_transform(data)

    return nmf, nmf_array

def k_estimate_ac(data, nmf_array):

    import numpy as np
    from sklearn.cluster import AgglomerativeClustering as AC
    from sklearn.preprocessing import Normalizer
    from sklearn.metrics import normalized_mutual_info_score as nmis

    documents = data.shape[0]

    norm2 = Normalizer('l2')
    data = norm2.fit_transform(data)

    dissimilarity = np.ones([documents, documents], dtype = np.float) - data.dot(data.T)

    k = nmf_array.shape[1]

    ac = AC(k, affinity = 'precomputed', linkage = 'average')
   
    labels_ac = ac.fit_predict(dissimilarity)
    labels_nmf = [np.argmax(x) for x in nmf_array]

    return nmis(labels_ac, labels_nmf)

# Estimación del número de tópicos a partir de la comparación
# entre los resultados dados por NMF para distintas semillas
def k_estimate_autoconsistent(data, nmf_array, nseeds = 2, seed = 1234567):

    from sklearn.decomposition import NMF
    import numpy as np
    from sklearn.preprocessing import Normalizer
    from sklearn.metrics import normalized_mutual_info_score as nmis

    norm2 = Normalizer('l2')
    data = norm2.fit_transform(data)

    labels_per_seed = []
    labels_per_seed.append([np.argmax(x) for x in nmf_array])
    
    k = nmf_array.shape[1]
    np.random.seed(seed)
    for random_state in np.random.randint(0, 10**6, nseeds):

        nmf = NMF(k, random_state = random_state)

        nmf_array = nmf.fit_transform(data)
        labels_per_seed.append([np.argmax(x) for x in nmf_array])

    return np.mean([nmis(labels_per_seed[i], labels_per_seed[j]) for i in range(len(labels_per_seed)) for j in range(i+1, len(labels_per_seed))])


# Estimación del número de tópicos k a partir de observar la orthogonalidad
# entre los tópicos emergentes
def k_estimate_orthogonality(nmf):

    import numpy as np
    from sklearn.preprocessing import Normalizer

    norm2 = Normalizer('l2')

    components = norm2.fit_transform(nmf.components_)
    k = len(components)
        
    comp_orth = np.mean([components[i].dot(components[j]) for i in range(k) for j in range(i+1, k)])

    return comp_orth


def k_estimate_ac_and_ortho(data, k = 2, seed = 123457):

    nmf, nmf_array = nmf_array_seed(data, k, seed)

    comp_orth = k_estimate_orthogonality(nmf) 
    nmis = k_estimate_ac(data, nmf_array)
    autocons = k_estimate_autoconsistent(data, nmf_array)

    return nmis, autocons, comp_orth




