"""
Simple graph structure (undirected, not weighted).
Stores information about each user's connections and the user groups they're a part of.
"""

class Graph:
    graph_id = None  # ID number

    neighbors = {}
    # dict where a key is a node and its value is a set of its neighbors.
    # (x,y) -> x is in y's neighbors list and y is in x's neighbors list.

    groups = {}
    # Dict where a key is a node and its value is a set of groups it's in,
    # represented by sequential group identifiers.

    
    """
    class initializer
    """
    def __init__(self, graph_id = -1, edges = None):
        self.graph_id = graph_id

        if edges is not None:
            for edge in edges:
                self.add_edge(edge[0], edge[1])

    """
    representation (for clearer visualization and debugging)
    """
    def __repr__(self):
        output = "CONNECTIONS:\n"

        for n in self.neighbors:
            output += " " + str(n) + ": " + str(self.neighbors[n]) + "\n"

        output += "\nGROUPS:\n"

        for n in self.groups:
            output += " " + str(n) + ": " + str(self.groups[n]) + "\n"

        output += "\n"
        return output

    """
    add an undirected edge between x and y
    (if it doesn't already exist and if x != y)
    """
    def add_edge(self, x, y):
        if x == y:
            print("ERROR: You can't add a loop (edge from a node to itself).")
            return
      
        if x not in self.neighbors:
            self.neighbors[x] = set() # create x's neighbors set

        if y not in self.neighbors:
            self.neighbors[y] = set() # create y's neighbors set

        if x not in self.neighbors[y]:
            self.neighbors[y].add(x) # add x to y's neighbors set

        if y not in self.neighbors[x]:
            self.neighbors[x].add(y) # add y to x's neighbors set

    """
    add an user group
    receives the group ID and members list, and adds the group to all the members' groups sets
    """
    def add_group(self, group_id, members = None):
        if members is None:
            members = []

        for node in members:
            if node not in self.groups:
                self.groups[node] = set()

            self.groups[node].add(group_id)

    """
    returns the amount of neighbors a given node has
    """
    def neighbor_count(self, node):
        if node in self.neighbors:
            return len(self.neighbors[node])
        
        else:
            return 0

    """
    returns the amount of groups a given node is a member of
    """
    def group_count(self, node):
        if node in self.groups:
            return len(self.groups[node])
        
        else:
            return 0