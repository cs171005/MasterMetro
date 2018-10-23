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
"""
def dissatisfaction(origin, destination, bolttt, ttt, claim_file):
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
        #same train number.
        if bolttt[origin[1]][origin[0]]:
            if origin[0]%2 == 0:
                #when origin node is the deperture node.
                dissatisfaction_weight += claim_file[origin_station_number]["deperture_delay"]
            else:
                dissatisfaction_weight += claim_file[origin_station_number]["arrival_delay"]

            if ttt[destination[1]][destination[0]] - ttt[origin[1]][origin[0]] > 0:
                # corresponding to increase in stop time at the previous edge.
                dissatisfaction_weight += claim_file[origin_station_number]["hold_time_increasement"]

        if bolttt[destination[1]][destination[0]]:
            if destination[0]%2 == 0:
                #when origin node is the arrive node.
                dissatisfaction_weight += claim_file[destination_station_number]["deperture_delay"]
            else:
                dissatisfaction_weight += claim_file[destination_station_number]["arrival_delay"]

            if ttt[destination[1]][destination[0]] - ttt[origin[1]][origin[0]] > 0:
                # corresponding to increase in running time at the previous edge.
                dissatisfaction_weight += claim_file[origin_station_number]["running_time_increasement"]
    else:
        # diffrence train number.
        if origin[0] == destination[0] and origin[0]%2 != 0:
            # vertical connection between arrival nodes.
            if bolttt[origin[1]][origin[0]] and bolttt[destination[1]][destination[0]]:
                # * ← delayed
                # |
                # * ← delayed
                if abs(ttt[origin[1]][origin[0]] - ttt[destination[1]][destination[0]]) != 0:
                    dissatisfaction_weight += claim_file[destination_station_number]["frequency"]
            elif bolttt[destination[1]][destination[0]]:
                # @ ← not delayed
                # |
                # * ← delayed
                dissatisfaction_weight += claim_file[destination_station_number]["frequency"]

    return dissatisfaction_weight
"""
def exponential_dist(x,lam):
    return lam * np.e ** (-lam*x)

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
        # c_components = {"deperture_delay":42,"arrival_delay":42,"hold_time_increasement":44,"running_time_increasement":45,"frequency":46,"transit_connection":47}
        c_components = {"deperture_delay":180,"arrival_delay":180}
        claim_file[st] = c_components

    ddd = 1.0
    nx.set_edge_attributes(gp, ddd, 'weight')
    nx.set_edge_attributes(gp, -1*ddd, 'negative_weight')

    # criterior = 180
    bolttt,rawttt = TFS.runWithDelayDissatisfactionBool(claim_file)
    # print len(bolttt[0]),len(bolttt)

    print len(bolttt), len(bolttt[0])
    for eg in gp.edges(data = True):
        if eg[0] in cost_dict:
            if eg[1] in cost_dict[eg[0]]:
                 eg[2]['weight'] = cost_dict[eg[0]][eg[1]]
                # eg[2]['negative_weight'] = -1*cost_dict[eg[0]][eg[1]]

        # print eg
        print eg[0], eg[1], eg[2]['weight']
        # print dissatisfaction(eg[0], eg[1], bolttt, rawttt, claim_file)
        # eg[2]['weight'] += dissatisfaction(eg[0], eg[1], bolttt, rawttt, claim_file)
        penalty = 0.0
        modified_p = 0.0
        if bolttt[eg[0][1]][eg[0][0]]:
            if bolttt[eg[1][1]][eg[1][0]]:
                # eg[0]:true, eg[1]:true
                gp.node[eg[0]]['color'] = 'green'
                gp.node[eg[1]]['color'] = 'green'
            else:
                # eg[0]:true, eg[1]:false
                gp.node[eg[0]]['color'] = 'green'
        elif bolttt[eg[1][1]][eg[1][0]]:
            # eg[0]:false, eg[1]:true
            gp.node[eg[1]]['color'] = 'green'

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
    # plt.show()
    
    """
    delayed_t = []
    for r in range(len(bolttt)):
        print bolttt[r]
        print r, True in bolttt[r]
        if True in bolttt[r]:
            delayed_t.append(r)
    print delayed_t

    weight = list(map(lambda x: x - delayed_t[0], delayed_t))
    weight = list(map(lambda x: exponential_dist(x,.35), weight))
    weight = list(map(lambda x: x/sum(weight), weight))
    print weight
    print sum(weight)

    rescheduled_train_num = np.random.choice(delayed_t, p = weight)

    delayed_node = []
    print len(bolttt[rescheduled_train_num])
    for r in range(len(bolttt[rescheduled_train_num])):
        print bolttt[rescheduled_train_num][r]
        # print r, True in bolttt[rescheduled_train_num][r]
        if True == bolttt[rescheduled_train_num][r]:
            delayed_node.append(r)
    print delayed_node

    weight2 = list(map(lambda x: x - delayed_node[0], delayed_node))
    weight2 = list(map(lambda x: exponential_dist(x,.35), weight2))
    weight2 = list(map(lambda x: x/sum(weight2), weight2))
    print weight2
    print sum(weight2)

    rescheduled_node_num = np.random.choice(delayed_node, p = weight2)

    rt = []
    rn = []
    for i in range(100):
        rescheduled_train_num = np.random.choice(delayed_t, p = weight)

        delayed_node = []
        print len(bolttt[rescheduled_train_num])
        for r in range(len(bolttt[rescheduled_train_num])):
            print bolttt[rescheduled_train_num][r]
            # print r, True in bolttt[rescheduled_train_num][r]
            if True == bolttt[rescheduled_train_num][r]:
                delayed_node.append(r)
        print delayed_node

        weight2 = list(map(lambda x: x - delayed_node[0], delayed_node))
        weight2 = list(map(lambda x: exponential_dist(x,.35), weight2))
        weight2 = list(map(lambda x: x/sum(weight2), weight2))
        print weight2
        print sum(weight2)

        rescheduled_node_num = np.random.choice(delayed_node, p = weight2)

        rt.append(rescheduled_train_num)
        rn.append(rescheduled_node_num)

    print rt
    print rn

    fig = plt.figure()

    ax = fig.add_subplot(1,1,1)

    ax.scatter(rn,rt)

    ax.set_title('first scatter plot')
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    fig.show()


    result = []
    for i in range(0,1000):
        result.append(np.random.choice(delayed_t, p = weight))
    plt.hist(result)
    plt.show()
    """
