# -*- coding: utf-8 -*-
# https://qiita.com/neka-nat@github/items/28cc0251414635e2acfd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rd
import random

from TrafficFlowSimulator import *

TFS = TrafficFlowSimulator()

num_of_station = 19
claim_file = {}
for st in range(num_of_station):
    # c_components = {"deperture_delay":42,"arrival_delay":42,"hold_time_increasement":44,"running_time_increasement":45,"frequency":46,"transit_connection":47}
    c_components = {"deperture_delay":180,"arrival_delay":180,"hold_time_increasement":30,"running_time_increasement":90}
    claim_file[st] = c_components

bool,raw,ccc = TFS.runWithDelayDissatisfactionBool(claim_file)

for bl in range(len(bool)):
    print bool[bl]

for cc in range(len(ccc)):
    print ccc[cc]


"""
delayed_t = []
for r in range(len(bool)):
    print bool[r]
    print r, True in bool[r]
    if True in bool[r]:
        delayed_t.append(r)
print delayed_t

def exponential_dist(x):
    lam = .35
    return lam * np.e ** (-lam*x)

fig = plt.figure()

ax = fig.add_subplot(1,1,1)

ax.scatter(rn,rt)

ax.set_title('first scatter plot')
ax.set_xlabel('x')
ax.set_ylabel('y')

fig.show()
"""
