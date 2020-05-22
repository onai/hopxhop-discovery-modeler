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
    import matplotlib as plt

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.show()

def ambient_peer_discovery(G):

    H = {}
    for i in G.nodes():
        H[i] = [n for n in G.neighbors(i)]

    return H

if __name__== "__main__":

    n = int(sys.argv[1])
    N = int(sys.argv[2])
    ds = int(sys.argv[3])
    de = int(sys.argv[4])

    print("Generating for")
    print(sys.argv)

    G = generate_graph(ds, de, N)


    H = ambient_peer_discovery(G)


    for i in range(N, n+N):

        # add a new node
        G.add_node(i)

        # pick a random node in the network and add and undirected edge to the new node
        random_node = random.randint(0, N)
        G.add_edge(random_node, i)
        G.add_edge(i, random_node)

        # find shortest path (bfs?) from source every node to new node
        print("Average hops for ", i, ": ",  numpy.mean(dict(nx.single_target_shortest_path_length(G, i)).values()))



