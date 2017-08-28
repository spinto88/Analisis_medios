from stacked_graph import *
import numpy as np

data = []
folder = 'Pagina12_politica_marzo'
n = 5

for topic in np.random.choice(range(40), 10): #[2, 11, 36, 8, 28]: #range(40):

    topic_profile = np.genfromtxt('{}/topic{}_temp.csv'.format(folder,topic),\
                                  delimiter = ',', skip_header = 1, \
                                  dtype = None)

    topic_weigth = [i[1] for i in topic_profile]

    topic_weigth_norm = []
    if n != 0:
      for i in range(n):
        topic_weigth_norm.append(np.trapz(topic_weigth[:i+n+1]))
      for i in range(n, len(topic_weigth) - n):
        topic_weigth_norm.append(np.trapz(topic_weigth[i-n:i+n+1]))
      for i in range(len(topic_weigth) - n, len(topic_weigth)):
        topic_weigth_norm.append(np.trapz(topic_weigth[i-n:]))
      data.append(topic_weigth_norm)
    else:
      data.append(topic_weigth)

#print sorted(range(40), key = lambda x: np.trapz(data[x]), reverse = True)[:5]

#exit()
      
stacked_graph(data, normed = True)

