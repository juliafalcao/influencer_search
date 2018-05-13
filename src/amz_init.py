"""
Initializes the full graph for the Amazon dataset with all the users (nodes)
and connections (edges) between them and the groups each one is a part of.
"""

from graph import *
import sys
import os
from subprocess import check_output


def build_graph():
    graph = Graph()

    # edges
    try:
        f = open("data/amazon/edges.txt")

        for line in f:
            if "#" in line:
                continue

            nodes = line.strip().split("\t")
            graph.add_edge(int(nodes[0]), int(nodes[1]))

        f.close()

    except IOError:
        print("Could not open 'data/amazon/edges.txt'.")
        return
    
    # groups
    try:
        f = open("data/amazon/groups.txt")
        i = 0

        for line in f:
            members = [int(m) for m in line.strip().split("\t")]
            graph.add_yt_group(i, members)
            i += 1

        f.close()

    except IOError:
        print("Could not open 'data/amazon/groups.txt'.")
        return

    return graph