# -*- coding: utf-8 -*-
# https://qiita.com/neka-nat@github/items/28cc0251414635e2acfd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from TrafficFlowSimulator import *

TFS = TrafficFlowSimulator()

ttt = TFS.runWithDelayDissatisfactionBool(180)
