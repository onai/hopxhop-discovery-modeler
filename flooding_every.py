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



if __name__== "__main__":

    d = int(sys.argv[1])
    N = int(sys.argv[2])
    ds = int(sys.argv[3])
    de = int(sys.argv[4])
    newNodes = int(sys.argv[5])

    #print("Generating for")
    #print(sys.argv)

    G = generate_graph(ds, de, N)

    # add random weights
    for i, j in G.edges():
        rand_weight = random.randint(1,10)
        G.remove_edge(i, j)
        #G.remove_edge(j, i)
        G.add_edge(i, j, weight=rand_weight)
        G.add_edge(j, i, weight=rand_weight)


    for i in range(N, newNodes+N):

        # add a new node
        G.add_node(i)

        # pick a random node in the network and add and undirected edge to the new node
        random_node = random.randint(0, N)
        G.add_edge(random_node, i)
        G.add_edge(i, random_node)

    ##
    ##
    ##  SCENARIO 2b: Random radius
    ##
    ##

    level_mean = []
    messages_list = []
    
    pre_visited = {}
    pre_level = {}

    #pre-flood if depth > 1
    for n in G.nodes():

        if d > 1:

            # each node knows other nodes up to some radius so previsit till some depth
            #pre_visit_neighbor_list = [i for i in ]
            #while not all(i==1 for i in pre_visited):
            tmp_depth = 1
            tmp_queue = [n, None]
            pre_visited[n] = [0 for i in range(N+newNodes)]
            pre_level[n] = [math.inf for i in range(N+newNodes)]

            while tmp_depth != d:

                if not tmp_queue:
                    break

                ele = tmp_queue.pop(0)

                if ele is None:
                    tmp_depth += 1
                    continue

                pre_visited[n][ele] = 1
                pre_level[n][ele] = tmp_depth

                neigh = list(G.neighbors(ele))

                tmp_queue = tmp_queue + [i for i in neigh if i not in tmp_queue and pre_visited[n][i]!= 1]

                if tmp_queue[0] is None:
                    tmp_queue.append(None)


    #import  ipdb ; ipdb.set_trace()

    # Flood until you find N
    for n in G.nodes():
        visited = [0 for i in range(N+newNodes)]
        level = [math.inf for i in range(N+newNodes)]
        depth = 1
        queue = [n, None]

        messages = 0

        #import ipdb ; ipdb.set_trace()
        while not all(i==1 or i==2 for i in visited):

            if not queue:
                break

            ele = queue.pop(0)

            if ele is None:
                depth += 1
                continue

            messages += 1

            visited[ele] = 1
            level[ele] = depth

            # For the visited node, visit all the nodes it has pre-visited.
            # you'll visit those nodes for free because it has already been
            # visited before. It will not cost you messages, but it will cost
            # you time if you were to look for neighbors through it
            for i, j in enumerate(pre_level[ele]):
                #
                if j != math.inf:
                    visited[i] = 2
                    level[i] = depth + j


            neigh = list(G.neighbors(ele))

            # don't add duplicates and visited
            queue = queue + [i for i in neigh if i not in queue and visited[i]!= 1]

            if queue[0] is None:
                queue.append(None)


        #import  ipdb ; ipdb.set_trace()
        level_mean.append(numpy.mean(level))
        messages_list.append(messages)
        #print("Average time for node ", n," to send messages to all nodes: ", numpy.mean(level))
        #print(visited, level)


    #print("Average time for ", N," nodes to send messages to every nodes: ", numpy.mean(level_mean))
    print(numpy.mean(level_mean), " ,", numpy.mean(messages_list))
