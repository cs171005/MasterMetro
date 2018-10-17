# -*- coding: utf-8 -*-
# https://qiita.com/neka-nat@github/items/28cc0251414635e2acfd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from TrafficFlowSimulator import *

num_of_station = 19
num_of_train = 85

def add_cross_edge(gp, shape):
    """
    2DGridのグラフに斜め方向のエッジを追加する
    """
    for node in list(gp.nodes()):
        # print node
        nx_node = (node[0] - 1, node[1] + 1)
        if 0 <= nx_node[0] and nx_node[1] <= shape[1]-1 :
            gp.add_edge(node, nx_node)

def remove_vertical_edge(gp, shape):
    # print gp.edges()
    for row in range(1,shape[1]):
        for col in range(0,shape[0]):
            # print row,col
            origin = (col,row)
            dest = (col,row-1)
            gp.remove_edge(origin, dest)

def remove_horizontal_edge(gp, shape):
    # print gp.edges()
    for row in range(0,shape[1]):
        for col in range(1,shape[0]):
            # print row,col
            origin = (col,row)
            dest = (col-1,row)
            gp.remove_edge(origin, dest)

def cost(a, b):
    """
    コスト関数
    """

    x1 = np.array(a, dtype=np.float32)
    x2 = np.array(b, dtype=np.float32)
    dist = np.linalg.norm(x1 - x2)
    # print "the cost between" +  + "is" +


    return dist + penalty

def dist(a, b):
    """
    ヒューリスティック関数
    """
    x1 = np.array(a, dtype=np.float32)
    x2 = np.array(b, dtype=np.float32)
    return np.linalg.norm(x1 - x2)

def dissatisfaction(origin, destination, bolttt, claim_file):
    dissatisfaction_weight = 0

    origin_station_number = 0
    destination_station_number = 0

    if origin[0]%2 == 0:
        origin_station_number = origin[0]/2
    else:
        origin_station_number = (origin[0]+1)/2

    if destination[0]%2 == 0:
        destination_station_number = destination[0]/2
    else:
        destination_station_number = (destination[0]+1)/2
    if origin[1] == destination[1]:
        if bolttt[origin[1]][origin[0]]:
            if origin[0]%2 == 0:
                dissatisfaction_weight += claim_file[origin_station_number]["deperture_delay"]
            else:
                dissatisfaction_weight += claim_file[origin_station_number]["arrival_delay"]

        if bolttt[destination[1]][destination[0]]:
            if destination[0]%2 == 0:
                dissatisfaction_weight += claim_file[destination_station_number]["deperture_delay"]
            else:
                dissatisfaction_weight += claim_file[destination_station_number]["arrival_delay"]

    return dissatisfaction_weight


if __name__ == '__main__':
    TFS = TrafficFlowSimulator()
    # ttt = TFS.runWithDelayMatrix()
    # compose PERT diagram
    g_dim = [2*(num_of_station-1), num_of_train]
    print g_dim
    gp = nx.grid_2d_graph(2*(num_of_station-1), num_of_train)
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
        c_components = {"deperture_delay":3000,"arrival_delay":3000,"hold_time_increasement":44,"running_time_incresement":45,"frequency":46,"transit_connection":47}
        claim_file[st] = c_components

    ddd = 1.0
    nx.set_edge_attributes(gp, ddd, 'weight')
    nx.set_edge_attributes(gp, -1*ddd, 'negative_weight')

    criterior = 180
    bolttt = TFS.runWithDelayDissatisfactionBool(criterior)
    # print len(bolttt[0]),len(bolttt)

    print len(bolttt), len(bolttt[0])
    for eg in gp.edges(data = True):
        if eg[0] in cost_dict:
            if eg[1] in cost_dict[eg[0]]:
                 eg[2]['weight'] = cost_dict[eg[0]][eg[1]]
                # eg[2]['negative_weight'] = -1*cost_dict[eg[0]][eg[1]]

        # print eg
        print eg[0], eg[1], eg[2]['weight']
        print dissatisfaction(eg[0], eg[1], bolttt, claim_file)
        eg[2]['weight'] += dissatisfaction(eg[0], eg[1], bolttt, claim_file)
        penalty = 0.0
        modified_p = 0.0
        if bolttt[eg[0][1]][eg[0][0]]:
            if bolttt[eg[1][1]][eg[1][0]]:
                # eg[0]:true, eg[1]:true

                gp.node[eg[0]]['color'] = 'green'
                gp.node[eg[1]]['color'] = 'green'

                # if eg[0][0]%2 == 0:
                #     modified_p += claim_file[eg[0][0]]["deperture_delay"]
                #     modified_p += claim_file[eg[1][0]]["arrival_delay"]
                # else:
                #     modified_p += claim_file[eg[0][0]]["arrival_delay"]
                #     modified_p += claim_file[eg[1][0]]["deperture_delay"]
                #
                # eg[2]['weight'] += modified_p
            else:
                # eg[0]:true, eg[1]:false
                gp.node[eg[0]]['color'] = 'green'
                # if eg[0][0]%2 == 0:
                #     modified_p += claim_file[eg[0][0]]["deperture_delay"]
                # else:
                #     modified_p += claim_file[eg[0][0]]["arriva_delay"]
                #
                # eg[2]['weight'] += modified_p
        elif bolttt[eg[1][1]][eg[1][0]]:
            # eg[0]:false, eg[1]:true
            gp.node[eg[1]]['color'] = 'green'
            # if eg[0][0]%2 == 0:
            #     modified_p += claim_file[eg[1][0]]["deperture_delay"]
            # else:
            #     modified_p += claim_file[eg[1][0]]["arriva_delay"]
            # eg[2]['weight'] += modified_p

        print  str(eg[0]) + " → " + str(eg[2]['weight']) + " → " + str(eg[1])

    for eg in gp.edges(data = True):
        if eg[0] in cost_dict:
            if eg[1] in cost_dict[eg[0]]:
                eg[2]['negative_weight'] = -1*eg[2]['weight']

    idcs = np.random.choice(len(gp.nodes()), int(5 * 5 * 0.2), replace=False)
    # print idcs

    # スタート・ゴール・障害物を設定する
    st, gl, obs = (0,0), (30,60), [list(gp.nodes())[i] for i in idcs[2:]]
    # st, gl, obs = (0,0), (np.random.randint(g_dim[0]),np.random.randint(g_dim[1])), [list(gp.nodes())[i] for i in idcs[2:]]
    obs = [list(gp.nodes())[i] for i in idcs[2:]]

    path = nx.astar_path(gp, st, gl, cost)
    length = nx.astar_path_length(gp, st, gl, cost)

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
            # longest_length += cost_dict[previous_nd][nd]
            longest_length += gp[previous_nd][nd]['weight']
            # print ('{0}-[{1}]→{2}'.format(previous_nd,cost_dict[previous_nd][nd],nd))
        previous_nd = nd

    print(path)
    print(length)

    for p in path[1:-1]:
        if gp.node[p].get('color', '') == 'black':
            print('Invalid path')
            continue
        gp.node[p]['color'] = 'blue'

    for p in path2[st][gl][:]:
        if gp.node[p].get('color', '') == 'black':
            print('Invalid path')
            continue
        gp.node[p]['color'] = 'orange'

    print"------------"
    print(path2[st][gl])
    print longest_length
    gp.node[st]['color'] = 'green'
    gp.node[gl]['color'] = 'red'
    for o in obs:
        gp.node[o]['color'] = 'black'

    #show the graph
    pos = dict((n, n) for n in gp.nodes())
    nx.draw(gp,
            pos,
            node_color=[gp.node[n].get('color', 'white') for n in gp.nodes()],
            node_size=20,
            edge_size=1)
    edge_labels = nx.get_edge_attributes(gp,'weight')
    # nx.draw_networkx_edge_labels(gp, pos, edge_labels)
    plt.axis('equal')
    plt.gca().invert_yaxis()

    outputFile = 'recordedPERTdiagram-'+datetime.datetime.now().strftime('%y%m%d-%H%M%S')+'.png'
    plt.savefig(outputFile)
    plt.show()
