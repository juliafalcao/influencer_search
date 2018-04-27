"""
Initializes the graphs for all the ego nodes.
Each graph is an ego graph. The ego is not represented in the graph but its user ID is the graph's ID.

"""

from graph import *
import sys, os
from subprocess import check_output

print(os.getcwd())

os.chdir("data")
ls = check_output("ls")
ego_files = [f.strip() for f in ls.split("\n")]
ego_files.remove("facebook_combined.txt")
ego_files.remove("readme-ego.txt")
ego_files.remove("")

ego_graphs = {} # dict of ego ID's and their respective graph structures

for file in ego_files:
    ego_id, data = file.split(".")
    

        ego_graphs[ego_id] = graph

    if data == "circles":
        try:
            f = open(file)
            lines = f.readlines()
            f.close()

        except IOError:
            # TODO: error msg
            exit

        for line in lines:
            members = [p.strip() for p in line.split("\t")]
            circle_id = int(members.pop(0).strip("circle"))
        






            
