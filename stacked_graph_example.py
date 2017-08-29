from stacked_graph import *
from auxiliar_functions import *
from temporal_profiles_plot import *
import numpy as np
import cPickle as pk

folder = 'LaNacion_politica_marzo'

fusion_labels = pk.load(file('{}/Fusion_labels.pk'.format(folder),'r'))

data = {}
for macro_topic in fusion_labels.keys():
  
  for topic in fusion_labels[macro_topic]:   

    try:
        data[macro_topic] += np.array(topic_means('{}/topic{}_temp.csv'.\
                        format(folder, topic), slide_window = 0)[1])
    except:
        data[macro_topic] = np.array(topic_means('{}/topic{}_temp.csv'.\
                        format(folder, topic), slide_window = 0)[1])
    

dates = topic_means('{}/topic{}_temp.csv'.format(folder, topic), \
                      slide_window = 3)[0]


macro_topics = fusion_labels.keys()
mean_topics = sorted(macro_topics, reverse = True, \
            key = lambda x: np.max(data[x]))[:5]

mean_topics += sorted(macro_topics, reverse = True, \
            key = lambda x: np.trapz(data[x]))[:5]

mean_topics = set(mean_topics)

data_aux = {}

for macro_topic in mean_topics:
  
  for topic in fusion_labels[macro_topic]:   

    try:
        data_aux[macro_topic] += np.array(topic_means('{}/topic{}_temp.csv'.\
                        format(folder, topic), slide_window = 0)[1])
    except:
        data_aux[macro_topic] = np.array(topic_means('{}/topic{}_temp.csv'.\
                        format(folder, topic), slide_window = 0)[1])


data_aux2 = []
for macro_topic in mean_topics:

    data_aux2.append(topic_means_signal(data_aux[macro_topic], slide_window = 3))

for macro_topic in mean_topics:
    print fusion_labels[macro_topic]


stacked_graph(data_aux2, dates, date_ticks = 3, normed = True, file2save = 'LaNacion_marzo_stacked.eps')
