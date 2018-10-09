# -*- coding: utf-8 -*-
# https://qiita.com/neka-nat@github/items/28cc0251414635e2acfd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from TrafficFlowSimulator import *

TFS = TrafficFlowSimulator()

ttt = TFS.runWithDelayMatrix()

criterior = 180

bolttt = []
for row in range(0,len(ttt)):
    blt = []
    for col in range(0,len(ttt[row])):
        if ttt[row][col] >= criterior:
            blt.append(True)
        else:
            blt.append(False)
    bolttt.append(blt)

for row in range(0,len(bolttt)):
    print bolttt[row]
