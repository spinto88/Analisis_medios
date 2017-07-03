import cPickle as pk
from sklearn.manifold import MDS
import numpy as np
import matplotlib.pyplot as plt

newspaper = 'lanacion'

number_of_topics = 62

notes = [pk.load(file('Data03-05/{}_topic{}_vect.pk'.format(newspaper, i),'r')) \
                for i in range(number_of_topics)]

diss_matrix = np.array([[np.abs(np.log(notes[i].dot(notes[j]))) \
                    for i in range(number_of_topics)]
                    for j in range(number_of_topics)])

mds = MDS(n_components = 2, dissimilarity = 'precomputed')
x_mds = mds.fit_transform(diss_matrix)

plt.scatter(x_mds[:,0], x_mds[:,1], alpha = 0.25, s = 100)
for i in range(number_of_topics):
    plt.text(x_mds[i,0], x_mds[i,1], str(i))
plt.grid('on')
plt.show()
