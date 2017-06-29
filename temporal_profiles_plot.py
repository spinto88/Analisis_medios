import matplotlib.pyplot as plt
import numpy as np
import datetime

def temporal_profile_plot(newspaper = 'lanacion', topic = 2, slide_window = 7, date_ticks = 15):

    topic_profile = np.genfromtxt('Data/lanacion_topic{}_temp.csv'.format(topic), \
                delimiter = ',', skip_header = 1, dtype = None)

    dates = [datetime.datetime.strptime(i[0], "%Y-%m-%d").date() for i in topic_profile]
    topic_weight = [i[1] for i in topic_profile]

    wm = slide_window
    x_axis = [range(i, i + wm)[wm/2] \
          for i in range(len(topic_weight) - wm - 1)]

    topic_means = np.array([np.mean(topic_weight[i:i+wm]) \
               for i in range(len(topic_weight) - wm - 1)], dtype = np.float)
    topic_means /= np.max(topic_means)

    plt.figure(1)
    plt.clf()
    plt.axes([0.15, 0.20, 0.75, 0.70])
    plt.plot(x_axis, topic_means, 'b-', linewidth = 2)
    plt.grid('on')
    plt.xticks(range(0, len(x_axis), date_ticks), \
              [dates[i] for i in range(0, len(x_axis), date_ticks)], \
               rotation = 'vertical')
    plt.ylim([0, 1.00])
    plt.ylabel('Topic relative weight', size = 20)
    plt.yscale('symlog')
    plt.title('{} - topic {}'.format(newspaper, topic), size = 20)
    plt.yticks([0, 0.1, 0.25, 0.5, 0.75, 1.00],\
           [0, 0.1, 0.25, 0.5, 0.75, 1.00], size = 15)
    plt.savefig('{}_topic{}.eps'.format(newspaper, topic))
