"""
Simple graph structure (undirected, not weighted).
"""

import sys

class Graph:
	graph_id = None # ID number

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
	Dict where a key is a circle ID and its value is a set of nodes in the circle.
	e.g. 
	"""

	# class constructor
	def __init__(self, graph_id = -1, edges = []):
		# input: a list of tuples (x,y) that represent an undirected edge between x and y
		
		if graph_id <= -1:
			print("Graph ID (ego ID) has to be greater than or equal to zero.")
			return
		
		self.graph_id = graph_id

		for edge in edges:
			x = edge[0]
			y = edge[1]

			self.add_edge(x,y)

	# representation (in ego-facebook dataset context)
	# for clearer visualization and debugging
	def __repr__(self):
		output = "<EGO: " + str(self.graph_id) + "\n\nCONNECTIONS:\n";

		for n in self.neighbors:
			output += " " +  str(n) + ": " + str(self.neighbors[n]) + "\n"

		output += "\nCIRCLES:\n";

		for n in self.groups:
			output += str(n) + ": " + str(self.groups[n]) + "\n"
		
		output += ">\n"

		return output

	# add an undirected edge from x to y if it doesn't already exist and x != y
	def add_edge(self, x, y):
		if (x == y):
			print("ERROR: You can't add a loop (edge from a node to itself).")
			return

		if x not in self.neighbors:
			self.neighbors[x] = set()

		if y not in self.neighbors:
			self.neighbors[y] = set()

		if x not in self.neighbors[y]:
			self.neighbors[y].add(x)
		
		if y not in self.neighbors[x]:
			self.neighbors[x].add(y)

	# returns the amount of neighbors a node has
	def neighbor_count(self, node):
		if node in self.neighbors:
			return len(self.neighbors[node])

	# returns the amount of groups a node is a part of
	def group_count(self, node):
		count = 0

		for g in self.groups:
			if node in self.groups[g]:
				count += 1

		return count