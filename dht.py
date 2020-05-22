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

    newNodes = int(sys.argv[1])
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


    tables = []
    for i in G.nodes():

        tables.append(Table(i, G, None))

    marktable = { j: [0 for i in range(N+1)] for j in range(N, newNodes+N)}
    #import ipdb ; ipdb.set_trace()
    for i in range(N, newNodes+N):
        # add a new node
        G.add_node(i)

        # pick a random node in the network and add and undirected edge to the new node
        random_node = random.randint(0, N)
        G.add_edge(random_node, i)
        G.add_edge(i, random_node)

        # update table of the random node
        try:
            tables[random_node].routes[random_node].append(i)
        except:
            #import ipdb ; ipdb.set_trace()
            pass

        # update new node's table
        tables.append(Table(i, G, 1))


        marktable[i][N] = 1
        marktable[i][random_node] = 1

    #import ipdb ; ipdb.set_trace()
    # Loop until everyone finds N
    messages = 0
    for time in range(100):
        for n in G.nodes():
            if n >= N:
                continue

            # look at your immediate neighbor and see if there's N
            for neighbors in tables[n].routes[n]:

                # If n has found all new nodes, stop
                if all(marktable[k][n] == 1 for k in range(N, newNodes+N)):
                    break

                messages += 1

                for j in range(N, newNodes+N):
                    if tables[neighbors].has(j):
                        try:
                            tables[n].routes[neighbors].append(j)
                        except:
                            #import ipdb ; ipdb.set_trace()
                            tables[n].routes[neighbors] = [j]
                        marktable[j][n] = 1

                    # If n has found all new nodes, stop
                    if all(marktable[k][n] == 1 for k in range(N, newNodes+N)):
                        break

        if all(sum(marktable[k]) == N+1 for k in marktable.keys()):
            print('Everyone found it! ', time, ". Total messages: ", messages)
            break
