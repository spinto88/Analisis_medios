# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import datetime

def temporal_profile(topic_file, slide_window = 7):

    topic_profile = np.genfromtxt(topic_file, \
            delimiter = ',', skip_header = 1, dtype = None)

    topic_weight = [i[1] for i in topic_profile]

    wm = slide_window
    x_axis = [range(i, i + wm)[wm/2] \
          for i in range(len(topic_weight) - wm - 1)]

    topic_means = np.array([np.mean(topic_weight[i:i+wm]) \
                  for i in range(len(topic_weight) - wm - 1)], \
                  dtype = np.float)

    return topic_means

topics_means = []
for topic in range(50):
    try:
        topic_file = 'Data01-03_01-06/pagina12_topic{}_temp.csv'.format(topic)
        topics_means.append(temporal_profile(topic_file))
    except:
        pass

def temporal_profile_plot(topic_file, slide_window = 7, date_ticks = 7, colour = 'b', title = 'Topic', target = 'Figure1.eps'):

    topic_profile = np.genfromtxt(topic_file, \
            delimiter = ',', skip_header = 1, dtype = None)

    dates = [datetime.datetime.strptime(i[0], "%Y-%m-%d").date() for i in topic_profile]

    topic_weight = [i[1] for i in topic_profile]

    wm = slide_window
    x_axis = [range(i, i + wm)[wm/2] \
          for i in range(len(topic_weight) - wm - 1)]

    return x_axis, dates

x_axis, dates = temporal_profile_plot('Data01-03_01-06/lanacion_topic0_temp.csv')

topics_means = np.array(topics_means)
A = np.argmax(topics_means, axis = 0)

plt.clf()
plt.axes([0.15, 0.20, 0.75, 0.70])
plt.plot(x_axis, A, 'r-', linewidth = 2)
plt.grid('on')
plt.xticks(range(0, len(x_axis), 7), \
          [dates[i] for i in range(0, len(x_axis), 7)], \
          rotation = 'vertical')
plt.ylabel(u'Número de tópico', size = 20)
plt.title(u'Página 12', size = 20)
plt.yticks(size = 20)
plt.savefig('principal_topic_pagina12.eps')
plt.show()
