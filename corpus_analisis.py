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

length_of_texts = [len(word_tokenize(text)) for text in texts_to_analize]

import numpy as np

print 'Valor medio: {}'.format(np.mean(length_of_texts))
print 'Desviacion: {}'.format(np.std(length_of_texts))

hist, edges = np.histogram(length_of_texts, bins = np.logspace(0, 4, 10), normed = True)

import matplotlib.pyplot as plt

plt.axes([0.20, 0.20, 0.70, 0.70])
plt.plot([(edges[i+1] * edges[i])**0.5 for i in range(len(hist))], hist, '.-', markersize = 15)
plt.grid('on')
plt.xlabel('Largo del texto (palabras)', size = 20)
plt.ylabel('Densidad de documentos', size = 20)
plt.xscale('log')
plt.yscale('log')
plt.xticks(size = 15)
plt.yticks(size = 15)
plt.text(2, 10**(-3.9), s = u'Valor medio: {}\nDesviación: {}'.\
         format(int(np.mean(length_of_texts)), int(np.std(length_of_texts))), size = 20)
plt.savefig('Largo_de_documentos.eps')
plt.show()

