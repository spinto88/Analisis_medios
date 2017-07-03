import cPickle as pk
import numpy as np
import matplotlib.pyplot as plt

number_of_topics = 29

newspaper = 'lanacion'
topics_ln = [pk.load(file('Data03-05/{}_topic{}_vect.pk'.format(newspaper, i),'r')) \
                for i in range(number_of_topics)]

newspaper = 'pagina12'
topics_p12 = [pk.load(file('Data03-05/{}_topic{}_vect.pk'.format(newspaper, i),'r')) \
                for i in range(number_of_topics)]

for i in range(number_of_topics):    
    print i, sorted([topics_ln[i].dot(t) for t in topics_p12], reverse = True)[0]
#    print i, sorted([topics_p12[i].dot(t) for t in topics_ln], reverse = True)[0]


