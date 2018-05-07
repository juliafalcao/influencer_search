"""
Simple graph structure (undirected, not weighted).
Stores information about each user's friends and the friend groups they're a part of.
"""

import sys


class Graph:
    graph_id = None  # ID number

    neighbors = {}

    """
    Dict where a key is a node and its value is a set of its neighbors, or nodes it's
    connected to by an edge.
    e.g. {1: [2, 3], 2: [1, 3], 3: [1, 2, 4], 4: [3]}
    node 1 has edges to nodes 2 and 3, node 2 has edges to nodes 1 and 3, and so on.
    Each edge is represented twice in this structure: (x,y) -> x is in y's neighbors list and
    y is in x's neighbors list.
    """

    groups = {}
    """
    Dict where a key is a node and its value is a set of groups it's in. Group information
    comes from separate ego networks and different groups can have the same group ID in
    different ego networks, therefore, a group is represented by a tuple (e, g) where e is
    the ego network and g is the group ID. So (107, 10) is group number 10 in node 107's
    ego network.
    """

    # class constructor
    def __init__(self, graph_id = -1, edges = None):
        if edges is None:
            edges = []

        self.graph_id = graph_id

        for edge in edges:
            self.add_edge(edge[0], edge[1])


    # representation
    # for clearer visualization and debugging
    def __repr__(self):
        output = "CONNECTIONS:\n"

        for n in self.neighbors:
            output += " " + str(n) + ": " + str(self.neighbors[n]) + "\n"

        output += "\GROUPS:\n"

        for n in self.groups:
            output += " " + str(n) + ": " + str(self.groups[n]) + "\n"

        output += "\n"

        return output

    # add an undirected edge from x to y if it doesn't already exist and if x != y
    def add_edge(self, x, y):
        if x == y:
            print("ERROR: You can't add a loop (edge from a node to itself).")
            return
      
      
        if x not in self.neighbors:
            self.neighbors[x] = set()
            #put x in neighbors dict
        if y not in self.neighbors:
            self.neighbors[y] = set()
            #put y in neighbors dict
        if x not in self.neighbors[y]:
            self.neighbors[y].add(x)
            #put x as neighbor of y in neighbors dict
        if y not in self.neighbors[x]:
            self.neighbors[x].add(y)
            #put y as neighbor of x in neighbors dict

    # add a friend group

    # facebook dataset: based on ego networks
    def add_fb_group(self, ego_id, group_id, members = None):
        if members is None:
            members = []
        
        for node in members:
            if node not in self.groups:
                self.groups[node] = set()

            self.groups[node].add((ego_id, group_id))

    # youtube dataset
    def add_yt_group(self, group_id, members = None):
        if members is None:
            members = []

        for node in members:
            if node not in self.groups:
                self.groups[node] = set()

            self.groups[node].add(group_id)

    # returns the amount of neighbors a node has
    def neighbor_count(self, node):
        if node in self.neighbors:
            return len(self.neighbors[node])

    # returns the amount of groups a node is a part of
    def group_count(self, node):
        if node in self.groups:
            return len(self.groups[node])
        
        else:
            return 0

    """
    def nodes_not_in_groups(self):
        nodes = []

        for node in self.neighbors.keys():
            if node not in self.groups or len(self.groups[node]) == 0:
                nodes.append(node)
        
        nodes.sort()   
        return nodes
    """
