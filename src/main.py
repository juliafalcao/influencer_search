# -*- coding: utf-8 -*-

from graph import *
import yt_init
import random
import time
import sys, os

# heuristic function IDs
FRIENDS = 1
GROUPS = 2

# change working dir to ../influencer_search if it's set as ../influencer_search/src
if "src" in os.getcwd():
    os.chdir("..")


def main():
    # for testing
    h_id = FRIENDS
    k = 10
    
    start_time = time.time()
    graph = yt_init.build_graph()
    elapsed_time = time.time() - start_time
    print("=> runtime (graph construction): %0.3fs" % float(elapsed_time))

    
    print("\nRANDOM-RESTART HILL CLIMBING:")
    start_time = time.time()
    solution = search(graph, h_id, k)
    elapsed_time = time.time() - start_time
    print("\nsolution: " + str(solution))
    print("=> runtime (heuristic search): %0.3fs" % float(elapsed_time))
    
    
    print("\nEXACT DEPTH-FIRST SEARCH:")
    start_time = time.time()
    exact_solution = []
    for i in range(k):
        exact_solution.append(dfs(graph, h_id, exact_solution))

    elapsed_time = time.time() - start_time
    print("global maxima: " + str(exact_solution))
    print("=> runtime (exact search): %0.3fs" % float(elapsed_time))
    

# returns the node's heuristic value according to the given heuristic ID
def heuristic_function(heuristic_id, graph, node):
    if heuristic_id == FRIENDS:
        return graph.neighbor_count(node)
    
    elif heuristic_id == GROUPS:
        return graph.group_count(node)
    
    else:
        print("ERROR: Invalid heuristic ID.")
        return


# main search function
# decides initial node, runs hill climbing search iteratively with randomly chosen
# starting points, checks when to stop iterations
def search(graph, heuristic_id, k = 1):
    local_maxima = set() # all unique results found
    iterations = k * 5;
    it = 0 # iteration counter

    print("k = " + str(k))

    # for i in range(iterations):
    while it < iterations or len(local_maxima) < k:
        initial_node = random_node(graph)

        print("\n-- search iteration " + str(it+1))
        print("initial node: " + str(initial_node))

        local_max, value = hill_climbing(graph, initial_node, heuristic_id, local_maxima)

        print("local max: " + str(local_max))
        print("value: " + str(value))
        local_maxima.add((local_max, value))

        it += 1

    # influencers = list(set(influencers))
    # influencers.sort(key = get_value, reverse = True)
    # solution = [node for (node, value) in influencers[:k]]
    solution = list(local_maxima)
    solution.sort(key = get_value, reverse = True)
    solution = solution[:k]

    return solution


"""
# helper function for the hill climbing search
# receives a node and its graph and returns the best next node out of its neighbors
def next_node(graph, current_node, heuristic_id):
    neighbors = graph.neighbors[current_node]

    max_count = 0
    max_neighbor = None

    for n in neighbors:
        count = heuristic_function(heuristic_id, graph, n)

        if count >= max_count: # >: no sideways moves; >=: yes sideways moves
            max_count = count
            max_neighbor = n
    
    return (max_neighbor, max_count)
"""

# hill climbing search
def hill_climbing(graph, initial_node, heuristic_id, locals_found):
    if initial_node not in graph.neighbors:
        print("ERROR: Initial node given is not in graph.")
        return

    current = initial_node
    explored = set()
    
    while True:
        # (next, value) = next_node(graph, current, heuristic_id)
        # choose next node
        neighbors = graph.neighbors[current]
        max_count = 0
        max_neighbor = None

        for n in neighbors:
            if n not in explored:
                count = heuristic_function(heuristic_id, graph, n)

                if count >= max_count: # allows sideways moves
                    max_count = count
                    max_neighbor = n
        
        next, next_value = max_neighbor, max_count
        current_value = heuristic_function(heuristic_id, graph, current)

        if next is None or next_value < current_value:
            return current, current_value # end of search

        current = next
        explored.add(next)


# choose a random node from the graph
def random_node(graph):
    nodes = list(graph.neighbors.keys())
    return random.choice(nodes)


# reachable nodes
def reachable(graph, solution):
    reachable = set()
    stack = []
    
    for influencer in solution:
        stack.append(influencer)

        while stack:
            current = stack.pop()

            if current not in reachable:
                reachable.add(current)
                stack.extend(graph.neighbors[current] - reachable)
    
    return len(reachable)

# exact depth-first search
# returns the global maximum node, excluding the nodes in the excluded list
# as a (node, value) pair
def dfs(graph, heuristic_id, excluded):
    initial_node = random_node(graph)
    visited = set()
    stack = []

    for (node, value) in excluded:
        # add excluded nodes so they won't be visited during the search
        visited.add(node)

    max_value = 0
    global_max = None

    stack.append(initial_node)

    while stack:
        current = stack.pop()

        if current not in visited:
            value = heuristic_function(heuristic_id, graph, current)

            if value > max_value:
                max_value = value
                global_max = current

            visited.add(current)
            stack.extend(graph.neighbors[current] - visited)

    return (global_max, max_value)


"""
# exact depth-first search
# returns the n highest-valued nodes in the whole graph according to the chosen heuristic function
# as (node, value) tuples
def dfs(graph, heuristic_id, n = 1):
    initial_node = random_node(graph)
    visited = set()
    stack = []
    maxes = []

    stack.append(initial_node)

    while stack:
        current = stack.pop()

        if current not in visited:
            value = heuristic_function(heuristic_id, graph, current)
            maxes.append((current, value))

            visited.add(current)
            stack.extend(graph.neighbors[current] - visited)

    maxes.sort(key = get_value, reverse = True) # sort by value
    maxes = maxes[:n] # leave only the n first

    return maxes
"""

def get_value(node_value_pair):
    if len(node_value_pair) == 2:
        return node_value_pair[1]
        
    else:
        print("ERROR: get_value() should receive a tuple containing a node ID and the node's heuristic value.")


main()