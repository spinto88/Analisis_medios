# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import datetime

def topic_means(data, slide_window = 0):

    topic_profile = np.genfromtxt(data, delimiter = ',', \
                    skip_header = 1, dtype = None)

    topic_means_aux = [i[1] for i in topic_profile]
    dates = [datetime.datetime.strptime(i[0], "%Y-%m-%d").date() \
             for i in topic_profile]

    n = slide_window

    topic_means_norm = []
    if n != 0:
      for i in range(n):
        topic_means_norm.append(np.trapz(topic_means_aux[:i+n+1]))
      for i in range(n, len(topic_means_aux) - n):
        topic_means_norm.append(np.trapz(topic_means_aux[i-n:i+n+1]))
      for i in range(len(topic_means_aux) - n, len(topic_means_aux)):
        topic_means_norm.append(np.trapz(topic_means_aux[i-n:]))

      if data != None:
          return dates, topic_means_norm
      else:
          return topic_means_norm
    else:
        if data != None:
            return dates, topic_means_aux
        else:
            return topic_means_aux

def topic_means_signal(signal, slide_window = 0):

    topic_means_aux = signal

    n = slide_window

    topic_means_norm = []
    if n != 0:
      for i in range(n):
        topic_means_norm.append(np.trapz(topic_means_aux[:i+n+1]))
      for i in range(n, len(topic_means_aux) - n):
        topic_means_norm.append(np.trapz(topic_means_aux[i-n:i+n+1]))
      for i in range(len(topic_means_aux) - n, len(topic_means_aux)):
        topic_means_norm.append(np.trapz(topic_means_aux[i-n:]))

      return topic_means_norm
    else:
      return topic_means_aux

def temporal_profile(dates, topic_means, date_ticks = 3, \
                        colour = 'b', label = '', show = 'on', \
                        filename = None):

    topic_means_norm = topic_means / np.max(topic_means)

    plt.axes([0.15, 0.20, 0.75, 0.70])
    plt.grid('on')
    plt.plot(topic_means_norm, '{}-'.format(colour), linewidth = 2,\
                                             label = label)
    plt.xlim([0, len(topic_means_norm)])
    plt.xticks(range(0, len(dates), date_ticks), \
              [dates[i] for i in range(0, len(dates), date_ticks)], \
              rotation = 45)

    plt.ylim([0, 1.00])
    plt.ylabel('Topic relative weight', size = 20)
    plt.yscale('symlog')
    plt.yticks([0, 0.1, 0.25, 0.5, 0.75, 1.00],\
           [0, 0.1, 0.25, 0.5, 0.75, 1.00], size = 15)

    if label != '':
        plt.legend(loc = 'best')

    if filename != None:
        plt.savefig(filename)

    return None

"""
data = 'LaNacion_politica_feb_mar_abr/topic57_temp.csv'
dates, tm = topic_means(data, slide_window = 3)

#data = 'Pagina12_politica_feb_mar_abr/topic62_temp.csv'
#dates, tm2 = topic_means(data, slide_window = 0)

#tm = np.array(tm1) + np.array(tm2)

#tm = topic_means_signal(tm, slide_window = 3)

temporal_profile(dates, tm, date_ticks = 15, \
                        colour = 'b', label = '', show = 'on', \
                        filename = None)
plt.show()

"""
