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

def temporal_profile_plot(topic_file, topic_means, slide_window = 7, date_ticks = 7, colour = 'b', title = 'Topic', target = 'Figure1.eps'):

    topic_profile = np.genfromtxt(topic_file, \
            delimiter = ',', skip_header = 1, dtype = None)

    dates = [datetime.datetime.strptime(i[0], "%Y-%m-%d").date() for i in topic_profile]
    topic_weight = [i[1] for i in topic_profile]

    wm = slide_window
    x_axis = [range(i, i + wm)[wm/2] \
          for i in range(len(topic_weight) - wm - 1)]

    plt.clf()
    plt.axes([0.15, 0.20, 0.75, 0.70])
    plt.plot(x_axis, topic_means, '{}-'.format(colour), linewidth = 2)
    plt.grid('on')
    plt.xticks(range(0, len(x_axis), date_ticks), \
              [dates[i] for i in range(0, len(x_axis), date_ticks)], \
               rotation = 'vertical')
    plt.ylim([0, 1.00])
    plt.ylabel('Topic relative weight', size = 20)
    plt.yscale('symlog')
    plt.title(title, size = 20)
    plt.yticks([0, 0.1, 0.25, 0.5, 0.75, 1.00],\
           [0, 0.1, 0.25, 0.5, 0.75, 1.00], size = 15)
    plt.savefig(target)

maxims = []
for topic in range(50):
    try:
        topic_file = 'Data01-03_01-06/lanacion_topic{}_temp.csv'.format(topic)
        topic_means = temporal_profile(topic_file)
        maxims.append(np.max(topic_means))
    except:
        pass

max_topic_means = max(maxims)

for topic in range(50):
    try:
        topic_file = 'Data01-03_01-06/lanacion_topic{}_temp.csv'.format(topic)
        topic_means = temporal_profile(topic_file)
	temporal_profile_plot(topic_file, topic_means/max_topic_means,\
                              title = u'La Nación - Tópico: {}'.format(topic),
			      target = 'lanacion_topic{}.eps'.format(topic))
    except:
        pass
