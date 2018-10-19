# -*- coding: utf-8 -*-
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def add_cross_edge(gp, shape):
    """
    2DGridのグラフに斜め方向のエッジを追加する
    """
    for node in gp.nodes():
        nx_node = (node[0] + 1, node[1] + 1)
        if nx_node[0] < shape[0] and nx_node[1] < shape[1]:
            gp.add_edge(node, nx_node)
        nx_node = (node[0] + 1, node[1] - 1)
        if nx_node[0] < shape[0] and nx_node[1] >= 0:
            gp.add_edge(node, nx_node)

ngrid = 20
gp = nx.grid_graph(dim=[ngrid, ngrid])
add_cross_edge(gp, [ngrid, ngrid])
idcs = np.random.choice(len(gp.nodes()), int(ngrid * ngrid * 0.2), replace=False)
# スタート・ゴール・障害物を設定する
st, gl, obs = list(gp.nodes())[idcs[0]], list(gp.nodes())[idcs[1]], [list(gp.nodes())[i] for i in idcs[2:]]
gp.node[st]['color'] = 'green'
gp.node[gl]['color'] = 'red'
for o in obs:
    gp.node[o]['color'] = 'black'

def dist(a, b):
    print a, b
    """
    ヒューリスティック関数
    """
    x1 = np.array(a, dtype=np.float32)
    x2 = np.array(b, dtype=np.float32)
    return np.linalg.norm(x1 - x2)

def cost(a, b, k1=1.0, k2=10.0, kind='intsct'):
    """
    コスト関数
    """
    x1 = np.array(a, dtype=np.float32)
    x2 = np.array(b, dtype=np.float32)
    dist = np.linalg.norm(x1 - x2)
    if any([(a == o or b == o) for o in obs]):
        penalty = 1.0e6
    else:
        penalty = 0.0
    return dist + penalty

for u, v, d in gp.edges(data=True):
    d['weight'] = cost(u, v)

path = nx.astar_path(gp, st, gl, cost)
length = nx.astar_path_length(gp, st, gl, cost)
print(path)
print(length)
for p in path[1:-1]:
    if gp.node[p].get('color', '') == 'black':
        print('Invalid path')
        continue
    gp.node[p]['color'] = 'blue'

nx.draw(gp,
        pos=dict((n, n) for n in gp.nodes()),
        node_color=[gp.node[n].get('color', 'white') for n in gp.nodes()],
        node_size=200)
plt.axis('equal')
plt.show()
