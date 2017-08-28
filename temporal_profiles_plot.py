# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import datetime

def temporal_profile_gt(data, slide_window = 1, date_ticks = 3, colour = 'b',\
                          label = '', show = 'on', filename = None):

    topic_profile = np.genfromtxt(data, delimiter = ',', \
                    skip_header = 3, dtype = None)

    dates = [datetime.datetime.strptime(i[0], "%Y-%m-%d").date() for i in topic_profile]
    topic_weight = [i[1] for i in topic_profile]

    wm = slide_window
    x_axis = [range(i, i + wm)[wm/2] \
          for i in range(len(topic_weight) - wm + 1)]

    topic_means = np.array([np.mean(topic_weight[i:i+wm]) \
               for i in range(len(topic_weight) - wm + 1)], dtype = np.float)
    topic_means_norm = topic_means / np.max(topic_means)

    plt.axes([0.15, 0.20, 0.75, 0.70])
    plt.plot(x_axis, topic_means_norm, '{}-'.format(colour), linewidth = 2,\
                                             label = label)
    plt.grid('on')
    plt.xlim([0, len(x_axis) + 1])
    plt.xticks(range(0, len(x_axis) + 2, date_ticks), \
              [dates[i] for i in range(0, len(x_axis) + 2, date_ticks)], \
               rotation = 30)
    plt.ylim([0, 1.00])
    plt.ylabel('Topic relative weight', size = 20)
    plt.yscale('symlog')
    plt.yticks([0, 0.1, 0.25, 0.5, 0.75, 1.00],\
           [0, 0.1, 0.25, 0.5, 0.75, 1.00], size = 15)

    if filename != None:
        plt.savefig(filename)

    return topic_means, x_axis, \
           [dates[i] for i in range(0, len(x_axis), date_ticks)]


def temporal_profile(data, slide_window = 1, date_ticks = 3, colour = 'b',\
                          label = '', show = 'on', filename = None):

    topic_profile = np.genfromtxt(data, delimiter = ',', \
                    skip_header = 1, dtype = None)

    dates = [datetime.datetime.strptime(i[0], "%Y-%m-%d").date() for i in topic_profile]
    topic_weight = [i[1] for i in topic_profile]

    wm = slide_window
    x_axis = [range(i, i + wm)[wm/2] \
          for i in range(len(topic_weight) - wm + 1)]

    topic_means = np.array([np.mean(topic_weight[i:i+wm]) \
               for i in range(len(topic_weight) - wm + 1)], dtype = np.float)
    topic_means_norm = topic_means / np.max(topic_means)

    plt.axes([0.15, 0.20, 0.75, 0.70])
    plt.plot(x_axis, topic_means_norm, '{}-'.format(colour), linewidth = 2, \
                                              label = label)
    plt.grid('on')
    plt.xlim([0, len(x_axis) + 1])
    plt.xticks(range(0, len(x_axis) + 2, date_ticks), \
              [dates[i] for i in range(0, len(x_axis) + 2, date_ticks)], \
               rotation = 30)
    plt.ylim([0, 1.00])
    plt.ylabel('Topic relative weight', size = 20)
    plt.yscale('symlog')
    plt.yticks([0, 0.1, 0.25, 0.5, 0.75, 1.00],\
           [0, 0.1, 0.25, 0.5, 0.75, 1.00], size = 15)

    if filename != None:
        plt.savefig(filename)

    return topic_means, x_axis, \
           [dates[i] for i in range(0, len(x_axis), date_ticks)]
"""
temporal_profile_gt('GT_devido.csv', \
               show = 'on', slide_window = 3, colour = 'g',\
               label = 'Gt')
"""
foldername = 'Pagina12_politica_abril'
i = 1
data = temporal_profile('{}/topic{}_temp.csv'.format(foldername, i), \
                             show = 'on', slide_window = 3, colour = 'b', label = u'La Nación')[0]

i = 46
data = temporal_profile('{}/topic{}_temp.csv'.format(foldername, i), \
                             show = 'on', slide_window = 3, colour = 'r', label = u'La Nación')[0]
plt.show()
exit()

plt.title('Desafuero de De Vido', size = 20)
plt.legend(loc = 'best')
plt.savefig('DeVido_lanacion.eps')
plt.show()

temporal_profile_gt('GT_devido.csv', \
               show = 'on', slide_window = 3, colour = 'g', 
		label = 'Gt')

foldername = 'Pagina12_politica_julio'
i = 3
data = temporal_profile('{}/topic{}_temp.csv'.format(foldername, i), \
                             show = 'on', slide_window = 3, colour = 'r',\
                             label = u'Página 12')[0]
plt.legend(loc = 'best')

plt.title('Desafuero de De Vido', size = 20)
plt.savefig('DeVido_pagina12.eps')

plt.show()
