"""
Creates the full graph for the com-Youtube dataset with all the users (nodes)
and connections (edges) between them and the groups each one is a part of.
"""

from graph import *
import pandas as pd

"""
Function that builds the graph from a file containing the edges and a file containing the groups.
"""
def build_graph(edges_filename, groups_filename):
    graph = Graph()

    # edges
    try:
        f = open(edges_filename)

        for line in f:
            nodes = line.strip().split("\t")
            graph.add_edge(int(nodes[0]), int(nodes[1]))

        f.close()

    except IOError:
        print(f"Could not open '{edges_filename}'.")
        return

    # groups
    try:
        f = open(groups_filename)
        group_id = 0

        for line in f:
            members = [int(m) for m in line.strip().split("\t")]
            graph.add_group(group_id, members)
            group_id += 1

        f.close()

    except IOError:
        print("Could not open '../data/youtube/allcmty.txt'.")
        return

    return graph