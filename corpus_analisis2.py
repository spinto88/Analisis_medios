# -*- coding: utf-8 -*-
import sqlite3
import cPickle as pk

conn = sqlite3.connect('data.db')

c = conn.cursor()

c.execute('select title, body from lanacion where title IS NOT NULL and body IS NOT NULL')
content = [row[0] + row[1] for row in c]
c.execute('select title, body from pagina12 where title IS NOT NULL and body IS NOT NULL;')
content += [row[0] + row[1] for row in c]
conn.close()

import random
texts_to_analize = random.sample(content, 10000)

from nltk.tokenize import word_tokenize
from nltk import FreqDist

for text in texts_to_analize:
    try:
        freq_dist += [item[1] for item in FreqDist(word.lower() for word in word_tokenize(text)).items()]
    except:
        freq_dist = [item[1] for item in FreqDist(word.lower() for word in word_tokenize(text)).items()]

import numpy as np

print 'Valor medio: {}'.format(np.mean(freq_dist))
print 'Desviacion: {}'.format(np.std(freq_dist))

hist, edges = np.histogram(freq_dist, bins = np.logspace(0, 4, 10), normed = True)

import matplotlib.pyplot as plt

plt.axes([0.20, 0.20, 0.70, 0.70])
plt.plot([(edges[i+1] * edges[i])**0.5 for i in range(len(hist))], hist, '.-', markersize = 15)
plt.grid('on')
plt.xlabel(u'Frecuencia del término', size = 20)
plt.ylabel(u'Densidad de frecuencias', size = 20)
plt.xticks(size = 15)
plt.yticks(size = 15)
plt.xscale('log')
plt.yscale('log')
plt.text(200, 0.005, s = u'Valor medio: {}\nDesviación: {}'.\
         format(int(np.mean(freq_dist)), int(np.std(freq_dist))), size = 20)
plt.savefig('Frecuencia_de_palabras.eps')
plt.show()
