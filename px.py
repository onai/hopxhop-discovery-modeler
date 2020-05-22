from gen import *
import networkx as nx
import time
import numpy as np
import math
import argparse
import sys
import random
import numpy

# Usage:
#
# python flooding.py 5 50 3 4
# n  = 5     - 5 new nodes to be added
# N  = 50    - 50 established nodes
# ds = 3     - degree range start
# de = 4     - degree range end

def plotG(G):
    import matplotlib.pyplot as plt

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()


def ambient_peer_discovery(G):

    H = {}
    for i in G.nodes():
        neighbor_list =  [n for n in G.neighbors(i)]
        H[i] = {j:j for j in neighbor_list}

    return H


if __name__== "__main__":

    n = int(sys.argv[1])
    N = int(sys.argv[2])
    ds = int(sys.argv[3])
    de = int(sys.argv[4])

    print("Generating for")
    print(sys.argv)

    G = generate_graph(ds, de, N)

    # add random weights
    for i, j in G.edges():
        rand_weight = random.randint(1,10)
        G.remove_edge(i, j)
        #G.remove_edge(j, i)
        G.add_edge(i, j, weight=rand_weight)
        G.add_edge(j, i, weight=rand_weight)


    H = ambient_peer_discovery(G)

    #import ipdb ; ipdb.set_trace()
    #plotG(G)

    # pick a random starter node
    # import ipdb ; ipdb.set_trace()

    #for time in range(1, 100):
    #    H_old = H
    #    for node in G.nodes():
    #        # exchange tables and update most optimal
    #        for neighbor in H[node]:
    #            for entry in H[neighbor]:
    #                if G[H[neighbor][entry]]['weight'] < G[H[node][entry]]['weight']:
    #                    H[node][entry] = H[neighbor][entry]

    #    if H_old == H:
    #        print("stop! at ", time)

    print(nx.floyd_warshall(G))
