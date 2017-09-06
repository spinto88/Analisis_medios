import cPickle as pk
import codecs
import numpy as np
from temporal_profiles_plot import *
import datetime

fusion_labels = pk.load(file('Fusion_labels_sem.pk','r'))

topics_per_week = 5

macro_topics = {}

dates = [str(datetime.date(2017,1,02) + datetime.timedelta((i - 1) * 7)) for i in range(1, 31)]

for macro_topic in fusion_labels.keys():
        
  features_macro_topic = []
  macro_topic_weight = {}

  for sem in range(1, 31):
    macro_topic_weight[dates[sem - 1]] = 0
  
  for topic in fusion_labels[macro_topic]:   

    sem = (topic / topics_per_week) + 1

    fp = codecs.open('LaNacion_sem{}/features{}.txt'.format(sem, topic),\
                                                           'r','utf-8')
    features_macro_topic += fp.read().split(',')[:10]

    fp.close()

    macro_topic_weight[dates[sem - 1]] += int(np.trapz(np.array(topic_means('LaNacion_sem{}/topic{}_temp.csv'.\
                         format(sem, topic), slide_window = 0)[1])))


  fmt = list(set(features_macro_topic)) 
  fmt = sorted(fmt, reverse = True, \
                key = lambda x: features_macro_topic.count(x))

  macro_topic_weight['tags'] = ' -'.join(fmt[:10])

  macro_topics[macro_topic] = macro_topic_weight


fp = codecs.open('Data_macro_topics_lanacion.csv','a','utf8')
fp.write('Topic,Date,Weight,Tags\n')
for macro_topic in fusion_labels.keys():
  for sem in range(1,31):
    fp.write(u'{},{},{},{}\n'.format(macro_topic, dates[sem-1], \
                             macro_topics[macro_topic][dates[sem-1]], \
                             macro_topics[macro_topic]['tags']))
fp.close()
