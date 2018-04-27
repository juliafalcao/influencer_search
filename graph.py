"""
Simple graph structure (undirected, not weighted).
"""

import sys

class Node:
    node_id = None
    groups = []

    def __init__(self, node_id = -1):
        if node_id <= -1:
            print("Node ID has to be an integer greater than or equal to zero.")
            return
        
        self.node_id = node_id
        

class Graph:
    graph_id = None # ID number

    neighbors = {}
    """
    Dict where a key is a node and its value is a list of its neighbors, or nodes it's
    connected to by an edge.
    e.g. {1: [2, 3], 2: [1, 3], 3: [1, 2, 4], 4: [3]}
         node 1 has edges to nodes 2 and 3, node 2 has edges to nodes 1 and 3, and so on.
    Each edge is represented twice in this structure: (x, y) -> x is in y's neighbors list and
    y is in x's neighbors list.
    """

    groups = {}
    """
    Dict where a key is a circle ID and its value is a list of nodes in the circle.
    e.g. {1: ['173'], 2: ['155', '99', '327', '140', '116', '147', '144', '150', '270']}
    """

    def __init__(self, graph_id = -1, edges = []):
        # input: a list of tuples (x,y) that represent an undirected edge between x and y
        
        if graph_id <= -1:
            print("Graph ID (ego ID) has to be greater than or equal to zero.")
            return
        
        self.graph_id = graph_id

        for edge in edges:
            x = edge[0]
            y = edge[1]

            if (x == y): break # no loops

            if x not in self.neighbors:
                neighbors[x] = []

            if y not in self.neighbors:
                neighbors[y] = []

            neighbors[x].append(y)
            neighbors[y].append(x)
    
    def __repr__(self):
        return "<ego: " + str(self.graph_id) + ",\nconnections: " + str(self.neighbors) + ",\ncircles: " + str(self.groups) + ">"

