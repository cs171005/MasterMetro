# -*- coding: utf-8 -*-
# https://qiita.com/neka-nat@github/items/28cc0251414635e2acfd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from TrafficFlowSimulator import *


def add_cross_edge(gp, shape):
    """
    2DGridのグラフに斜め方向のエッジを追加する
    """
    for node in list(gp.nodes()):
        print node

        nx_node = (node[0] - 1, node[1] + 1)
        if 0 <= nx_node[0] and nx_node[1] <= shape[1]-1 :
            gp.add_edge(node, nx_node)

def remove_vertical_edge(gp, shape):
    # print gp.edges()
    for row in range(1,shape[1]):
        for col in range(0,shape[0]):
            print row,col
            origin = (col,row)
            dest = (col,row-1)
            gp.remove_edge(origin, dest)

def remove_horizontal_edge(gp, shape):
    # print gp.edges()
    for row in range(0,shape[1]):
        for col in range(1,shape[0]):
            print row,col
            origin = (col,row)
            dest = (col-1,row)
            gp.remove_edge(origin, dest)



ngrid = 5

# num_of_station = 19
# num_of_train = 40

num_of_station = 19
num_of_train = 85


g_dim = [1+2*(num_of_station-1), num_of_train]

gp = nx.grid_2d_graph(1+2*(num_of_station-1), num_of_train)
gp = gp.to_directed()

add_cross_edge(gp, g_dim)
remove_vertical_edge(gp, g_dim)
remove_horizontal_edge(gp, g_dim)

#costing (1:)
cost_dict = {}
for tr in range(num_of_train):
    for node_number in range(1+2*(num_of_station-1)):
        cost_around_each_node = {}
        if node_number%2 == 0:
            cost_around_each_node[(node_number-1,tr+1)] = 30

        if node_number + 1 != 1+2*(num_of_station-1):
            if node_number%2 == 0:
                #even node
                #travel time cost (even → odd except last node)
                cost_around_each_node[(node_number+1,tr)] = 180
            else:
                #odd node
                #stopping time cost (odd → even except last node)
                cost_around_each_node[(node_number+1,tr)] = 30

                #the capacity of each inter-stations.
                if tr + 1 != num_of_train:
                    #departure interval time
                    cost_around_each_node[(node_number-1,tr+1)] = 180

        if tr + 1 != num_of_train:
            #departure interval time
            cost_around_each_node[(node_number,tr+1)] = 300

        # print tr,node_number,cost_around_each_node
        cost_dict[(node_number,tr)] = cost_around_each_node

claim_file = {}
for st in range(num_of_station):
    c_components = {"deperture_delay":10*st,"arrival_delay":40,"hold_time_increasement":40,"running_time_incresement":40,"frequency":40,"transit_connection":40}
    claim_file[st] = c_components

ddd = 1.0
nx.set_edge_attributes(gp, ddd, 'weight')
nx.set_edge_attributes(gp, -1*ddd, 'negative_weight')

for eg in gp.edges(data = True):
    if eg[0] in cost_dict:
        if eg[1] in cost_dict[eg[0]]:
            eg[2]['weight'] = cost_dict[eg[0]][eg[1]]
            eg[2]['negative_weight'] = -1*cost_dict[eg[0]][eg[1]]

    # print eg
    # print eg[0], eg[1], eg[2]['weight']


idcs = np.random.choice(len(gp.nodes()), int(ngrid * ngrid * 0.2), replace=False)
print idcs

# スタート・ゴール・障害物を設定する
st, gl, obs = (0,0), (7,9), [list(gp.nodes())[i] for i in idcs[2:]]
# st, gl, obs = (0,0), (np.random.randint(g_dim[0]),np.random.randint(g_dim[1])), [list(gp.nodes())[i] for i in idcs[2:]]
obs = [list(gp.nodes())[i] for i in idcs[2:]]

def cost(a, b):
    """
    コスト関数
    """

    x1 = np.array(a, dtype=np.float32)
    x2 = np.array(b, dtype=np.float32)
    dist = np.linalg.norm(x1 - x2)
    # print "the cost between" +  + "is" +

    if any([(a == o or b == o) for o in obs]):
        penalty = 1.0e6
    else:
        # penalty = 0.0
        if a[0]%2 == 0:
            penalty = claim_file[(a[0]/2)]["arrival_delay"]
        else:
            penalty = claim_file[((a[0]/2)+1)]["deperture_delay"]

        print  str(a) + "→" + " " + str(penalty) + "→" + str(b)
        # print "normal penalty is here."
    return dist + penalty


def dist(a, b):
    """
    ヒューリスティック関数
    """
    x1 = np.array(a, dtype=np.float32)
    x2 = np.array(b, dtype=np.float32)
    return np.linalg.norm(x1 - x2)

path = nx.astar_path(gp, st, gl, cost)
length = nx.astar_path_length(gp, st, gl, cost)

print(path)
print(length)

for p in path[1:-1]:
    if gp.node[p].get('color', '') == 'black':
        print('Invalid path')
        continue
    gp.node[p]['color'] = 'blue'

path2 = nx.johnson (gp, weight='negative_weight')

print('johnson: {0}'.format(path2[st][gl]))


for p in path2[st][gl]:
    if gp.node[p].get('color', '') == 'black':
        print('Invalid path')
        continue
    gp.node[p]['color'] = 'orange'

previous_nd = st
longest_length = 0
for nd in path2[st][gl][:]:
    if not(previous_nd == st and nd == st):
        longest_length += cost_dict[previous_nd][nd]
        # print ('{0}-[{1}]→{2}'.format(previous_nd,cost_dict[previous_nd][nd],nd))
    previous_nd = nd

print longest_length



gp.node[st]['color'] = 'green'
gp.node[gl]['color'] = 'red'
for o in obs:
    gp.node[o]['color'] = 'black'

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


for n in gp.nodes():
    if n[0] < 36 and bolttt[n[1]][n[0]]:
        print n, bolttt[n[1]][n[0]]
        gp.node[n]['color'] = 'pink'


#show the graph
pos = dict((n, n) for n in gp.nodes())
nx.draw(gp,
        pos,
        node_color=[gp.node[n].get('color', 'white') for n in gp.nodes()],
        node_size=40,
        edge_size=1)
edge_labels = nx.get_edge_attributes(gp,'weight')
nx.draw_networkx_edge_labels(gp, pos, edge_labels)
plt.axis('equal')
plt.gca().invert_yaxis()

plt.show()
