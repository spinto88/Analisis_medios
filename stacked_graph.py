import numpy as np
from matplotlib import pyplot as plt

# the data must be a list of temporal profiles

def stacked_graph(data, normed = False):

    np.random.seed(123458)

    # Make a stack of all the data
    y = np.row_stack((data)) # shape documents per days

    # this call to 'cumsum' (cumulative sum), passing in your y data, 
    # is necessary to avoid having to manually order the datasets
    y_stack = np.cumsum(y, axis=0, dtype = np.float)   # an array with the same shape of y

    if normed == True:
        for i in range(y_stack.shape[1]):
            y_stack[:,i] /= np.max(y_stack[:,i])
    else:
        pass

    # x axis
    x = np.arange(y.shape[1]) 

    # Plot features
    ax1 = plt.axes([0.15, 0.15, 0.70, 0.70])

    for i in range(y_stack.shape[0] - 1):

      if i == 0:
        facecolor = (0.2, np.random.random(), np.random.random())
        ax1.fill_between(x, 0, y_stack[0,:], facecolor = facecolor, \
                         linewidth = 0.10, alpha=.7)
      else:
        facecolor = (0.2, np.random.random(), np.random.random())
        ax1.fill_between(x, y_stack[i,:], y_stack[i+1,:], \
                         facecolor = facecolor, linewidth = 0.10, alpha=.7)

    plt.xlim([0, len(x)-1])
    plt.yticks([])
    plt.show()
    #plt.savefig('prueba.eps')
