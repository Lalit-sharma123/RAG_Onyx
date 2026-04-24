import networkx as nx

graph = nx.Graph()

def add_relation(a, b):
    graph.add_edge(a, b)