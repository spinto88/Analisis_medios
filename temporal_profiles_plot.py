# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import datetime

def temporal_profile_plot(newspaper, topic, slide_window = 7, date_ticks = 7):

    if newspaper != 'google_trends':
        topic_profile = np.genfromtxt('Data03-05/{}_topic{}_temp.csv'.format(newspaper, topic), \
                delimiter = ',', skip_header = 1, dtype = None)
    elif newspaper == 'google_trends':
        topic_profile = np.genfromtxt('{}/{}.csv'.format(newspaper, topic), \
                delimiter = ',', skip_header = 3, dtype = None)

    dates = [datetime.datetime.strptime(i[0], "%Y-%m-%d").date() for i in topic_profile]
    topic_weight = [i[1] for i in topic_profile]

    wm = slide_window
    x_axis = [range(i, i + wm)[wm/2] \
          for i in range(len(topic_weight) - wm - 1)]

    topic_means = np.array([np.mean(topic_weight[i:i+wm]) \
               for i in range(len(topic_weight) - wm - 1)], dtype = np.float)
    topic_means /= np.max(topic_means)

    if newspaper == 'lanacion':
        colour = 'b'
        label = u'La Nación'
    elif newspaper == 'pagina12':
        colour = 'r'
        label = u'Página12'
    elif newspaper == 'google_trends':
        colour = 'k'
        label = u'Google'

    plt.axes([0.15, 0.20, 0.75, 0.70])
    plt.plot(x_axis, topic_means, '{}-'.format(colour), linewidth = 2, label = label)
    plt.grid('on')
    plt.xticks(range(0, len(x_axis), date_ticks), \
              [dates[i] for i in range(0, len(x_axis), date_ticks)], \
               rotation = 'vertical')
    plt.ylim([0, 1.00])
    plt.ylabel('Topic relative weight', size = 20)
    plt.yscale('symlog')
#    plt.title('{} - topic {}'.format(newspaper, topic), size = 20)
    plt.yticks([0, 0.1, 0.25, 0.5, 0.75, 1.00],\
           [0, 0.1, 0.25, 0.5, 0.75, 1.00], size = 15)
    #plt.savefig('{}_topic{}.eps'.format(newspaper, topic))
   

plt.figure(1)
#temporal_profile_plot("lanacion", topic = 10)
temporal_profile_plot("pagina12", topic = 5)
#temporal_profile_plot("google_trends", topic = "milagro_sala")
#plt.title('Topic: "Milagro Sala"', size = 20)
plt.legend(loc = 'best')
#plt.savefig('milagro_sala_temp_profile.eps')
plt.show()
