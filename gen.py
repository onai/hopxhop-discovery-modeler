import random 
import networkx as nx

# to generate graph without networkx:
# https://cs.stackexchange.com/questions/42156/generate-a-random-graph-with-geometrical-degree-distribution

# generate a random graph with degree between a and b
def generate_graph(degree_start=10, degree_end=15, size=5000):
#def generate_graph(degree_start=1000, degree_end=10000, size=100000):

    z=[random.randint(degree_start, degree_end) for i in range(size)]

    # if sum of degree sequence is odd, make it even
    if sum(z) % 2 != 0:
       z[random.randint(0, size)] += 1 

    G=nx.configuration_model(z)

    # remove self-loops and parallel edges
    G=nx.Graph(G)
    G.remove_edges_from(G.selfloop_edges())

    return G
