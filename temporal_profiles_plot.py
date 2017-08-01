# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import datetime

def temporal_profile(data, slide_window = 7, date_ticks = 3,\
                          show = 'on', filename = None):

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
    plt.plot(x_axis, topic_means_norm, '-', linewidth = 2)
    plt.grid('on')
    plt.xticks(range(0, len(x_axis), date_ticks), \
              [dates[i] for i in range(0, len(x_axis), date_ticks)], \
               rotation = 30)
    plt.ylim([0, 1.00])
    plt.ylabel('Topic relative weight', size = 20)
    plt.yscale('symlog')
    plt.yticks([0, 0.1, 0.25, 0.5, 0.75, 1.00],\
           [0, 0.1, 0.25, 0.5, 0.75, 1.00], size = 15)

    if filename != None:
        plt.savefig(filename)
    if show == 'on':
        plt.show()

    return topic_means, x_axis, \
           [dates[i] for i in range(0, len(x_axis), date_ticks)]

maxs = []
for i in range(10):
    try:
        maxs.append(np.sum(temporal_profile('LaNacion_marzo/topic{}_temp.csv'.format(i), show = 'on')[0]))
    except:
        pass

principal_topics = sorted(range(len(maxs)), reverse = True, key = lambda x: maxs[x])[:10]
print principal_topics
"""
j = 0
plt.clf()
for pt in principal_topics:
    data = temporal_profile('LaNacion_marzo/topic{}_temp.csv'.format(pt), show = 'off', slide_window = 1)
    try:
        temporal_matrix[j] = data[0]
        j += 1
    except:
        temporal_matrix = np.zeros([len(principal_topics), len(data[0])])
        temporal_matrix[j] = data[0]
        j += 1

plt.figure(2)
plt.axes([0.00, 0.20, 1.00, 0.70]) 
plt.imshow(np.array(temporal_matrix),\
           vmin = 0, vmax = np.max(temporal_matrix),
           extent = [0, 30, 0, temporal_matrix.shape[1]], interpolation = 'nearest',\
           cmap = 'bone_r')

print temporal_matrix.shape

topic_name = {1: 'solari', 3: 'eliminatorias', 4: u'(pr.) división', 12: 'champions', 18: 'mujeres', 19: 'venezuela', 22: 'londres', 23: 'libertadores', 53: 'macri', 125: 'cgt', 31: 'messi'}

plt.xticks(np.array(range(0, 31, 3)), data[2], rotation = 75)

plt.yticks(np.array(sorted(range(1, 30, 3), reverse = True)) + 1, [topic_name[i] for i in principal_topics])

plt.title(u'La Nación - Marzo 2017', size = 15)
plt.savefig('lanacion_marzo2017.eps')
plt.show()
"""
