"""
Initializes the graphs for all the ego nodes.
Each graph is an ego graph. The ego is not represented in the graph but its user ID is the graph's ID.
"""

from graph import *
import sys
import os
from subprocess import check_output


def get_ego_graphs():
    ego_files = os.listdir("data")
    ego_files.remove("facebook_combined.txt")
    ego_files.remove("readme-ego.txt")

    ego_graphs = {} # dict of ego ID's and their respective graph structures

    for file in ego_files:
        ego_id = int(file.split(".")[0])

        if ego_id not in ego_graphs:
            ego_graphs[ego_id] = Graph(ego_id)


    for ego_id in ego_graphs:
        graph = ego_graphs[ego_id]

        # circles
        filename = ".".join([str(ego_id), "circles"])
        try:
            f = open("data/" + filename)
            lines = f.readlines()
            if "" in lines: lines.remove("")
            f.close()

            for line in lines:
                circle_id = int(line[ : line.index("\t")].strip("circle"))
                members = [int(p.strip()) for p in line[line.index("\t"):].strip().split("\t")]
               
                graph.groups[circle_id] = members

        except IOError:
            print("ERROR: Could not open " + filename, file = sys.stderr)
            f.close()
            exit

        # edges
        filename = ".".join([str(ego_id), "edges"])
        try:
            f = open("data/" + filename)
            lines = f.readlines()
            if "" in lines: lines.remove("")
            f.close()

            for line in lines:
                nodes = line.split(" ")
                x, y = int(nodes[0].strip()), int(nodes[1].strip())
                graph.add_edge(x,y)

        except IOError:
            print("ERROR: Could not open " + filename, file = sys.stderr)
            f.close()
            exit

    return ego_graphs

# print(get_ego_graphs()[107])