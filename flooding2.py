import os
import numpy as np
from queue import Queue
import math

from gen import *
import networkx as nx
import time
import numpy as np
import math
import argparse
import sys
import random
import numpy



def get_degree_neighbors(G, src, degree):

    routes = dict(nx.bfs_successors(G, src, depth_limit=degree))

    n_degree_neighbors = []
    for i in routes:
        n_degree_neighbors.extend(routes[i])

    return n_degree_neighbors
            


if __name__== "__main__":

    d = int(sys.argv[1])
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


    ##
    ##
    ##  SCENARIO 2b: Random radius
    ##
    ##

    #tables = []
    #for i in G.nodes():
    #
    #    tables.append(Table(i, G, None))


    # add a new node
    G.add_node(N)

    # pick a random node in the network and add and undirected edge to the new node
    random_node = random.randint(0, N)
    G.add_edge(random_node, N)
    G.add_edge(N, random_node)

    # update table of the random node
    #tables[random_node].routes[random_node].append(N)

    # update new node's table
    #tables.append(Table(N, G, 1))

    marktable = [0 for i in range(N+1)]
    marktable[N] = 1
    marktable[random_node] = 1


    # Flood until you find N
    for n in G.nodes():

        succ_list = get_degree_neighbors(G, n, d)
        found = False

        hops = 0
        visited = [0 for i in range(N+1)]

        while succ_list:

            visited_node = succ_list.pop(0)

            if N == visited_node:
                found = True
                marktable[visited_node] = 1
                break

            if not visited[visited_node]:
                hops += 1
                succ_list = succ_list + [i for i in get_degree_neighbors(G, visited_node, d) if i not in succ_list]
                #succ_list.extend(get_degree_neighbors(G, visited_node, d))
                visited[visited_node] = True

        print("Node ", n, "found it after sending ", hops, " messages")

