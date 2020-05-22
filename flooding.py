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




class Table:
    #def __init__(self, src, dst, nxt):
    #   self.routes = [[src, dst, nxt]]

    def __init__(self, src, G, degree):

        self.routes = dict(nx.bfs_successors(G, src, depth_limit=degree))

    def has(self, x):

        for i in self.routes:
            for j in self.routes[i]:
                if j == x:
                    return True
        return False

        #for k in succs.keys():
        #    pred_weight = 0

        #    if k != src:
        #        pred_weight = G[src][k]

        #    for v in succs[k]:

        #        minw = math.inf
        #        try: 
        #            minw = self.routes[src][v][1]
        #        except:
        #            pass
        #        
        #        self.routes[src] = [v, min(pred_weight + G[k][v], minw)]


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


    ##
    ##
    ##  SCENARIO 2a
    ##
    ##

    tables = []
    for i in G.nodes():

        tables.append(Table(i, G, None))


    # add a new node
    G.add_node(N)

    # pick a random node in the network and add and undirected edge to the new node
    random_node = random.randint(0, N)
    G.add_edge(random_node, N)
    G.add_edge(N, random_node)

    # update table of the random node
    tables[random_node].routes[random_node].append(N)

    # update new node's table
    tables.append(Table(N, G, 1))

    marktable = [0 for i in range(N+1)]
    marktable[N] = 1
    marktable[random_node] = 1


    # Flood until you find N
    for n in G.nodes():

        succ_list = list(G.neighbors(n))
        found = False

        messages = 0
        visited = [0 for i in range(N+1)]

        while succ_list:

            visited_node = succ_list.pop(0)

            if N == visited_node:
                found = True
                marktable[visited_node] = 1
                break

            if not visited[visited_node]:
                messages += 1
                succ_list.extend(list(G.neighbors(visited_node)))
                visited[visited_node] = True

        print("Node ", n, "found it after sending ", messages, " messages")




    ## Loop until everyone finds N
    #for time in range(100):
    #    for n in G.nodes():
    #        if n == N:
    #            continue
    #        # look at your immediate neighbor and see if there's N
    #        for neighbors in tables[n].routes[n]:
    #            if N in tables[neighbors].routes[neighbors]:
    #                tables[n].routes[neighbors].append(N)
    #                marktable[n] = 1
    #                break
    #            elif tables[neighbors].has(N):
    #                tables[n].routes[neighbors].append(N)
    #                marktable[n] = 1
    #                break

    #    if sum(marktable) == (N+1):
    #        print('Everyone found it! ', time)
    #        break

