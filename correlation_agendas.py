import cPickle as pk
import datetime
import os
from sklearn.preprocessing import Normalizer
from copy import deepcopy
import numpy as np

norm2 = Normalizer('l2')
newspaper = 'lanacion'

date = datetime.date(2017, 03, 1)
final_date = datetime.date(2017, 06, 1)

data = []

while date <= final_date:

 for newspaper in ['lanacion', 'pagina12']:

  topics = []
  for i in range(50):
    try:
      topics.append(pk.load(\
      file('{}_week{}/{}_topic{}_vect.pk'.format(newspaper, date, newspaper,i),'r'))) 
    except:
      pass

  topics = norm2.fit_transform(topics)

  if newspaper == 'lanacion':
      topics1 = deepcopy(topics)
  else:
      topics2 = deepcopy(topics)

 data.append([date, np.mean(np.max(topics1.dot(topics2.T), axis = 0)),\
              np.std(np.max(topics1.dot(topics2.T), axis = 0))])

 date += datetime.timedelta(7)

import matplotlib.pyplot as plt

plt.axes([0.15, 0.20, 0.75, 0.70])
#plt.errorbar(range(len(data)), [x[1] for x in data], [x[2] for x in data], fmt = '.-', markersize = 20)
plt.plot(range(len(data)), [x[1] for x in data], '.-', markersize = 20)
plt.grid('on')
plt.title('Comparacion Top 5 semanales', size = 20)
plt.ylabel('Similitud entre agendas', size = 20)
plt.yticks(size = 20)
plt.xticks(range(len(data)), [str(x[0] + datetime.timedelta(4)) for x in data], rotation = 90)
plt.savefig('Similitud_entre_agendas.eps')
plt.show()
