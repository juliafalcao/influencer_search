# -*- coding: utf-8 -*-

from graph import *
import yt_init
import random
import time
import sys, os

# heuristic function IDs
FRIENDS = 1
GROUPS = 2

# whether to print debug stuff or not
DEBUG = False

def main():
    # for testing
    h_id = FRIENDS
    
    # build graph
    start_time = time.time()
    graph = yt_init.build_graph()
    elapsed_time = time.time() - start_time
    print("=> runtime (graph construction): %0.4fs" % float(elapsed_time))

    
    # run random-restart hill climbing search
    print("\nRANDOM-RESTART HILL CLIMBING:")
    start_time = time.time()
    solution = search(graph, h_id)
    elapsed_time = time.time() - start_time
    print("solution: " + str(solution))
    print("=> runtime (heuristic search): %0.3fs" % float(elapsed_time))
    
    """
    # run exact depth-first search
    print("\nEXACT DEPTH-FIRST SEARCH:")
    start_time = time.time()
    exact_solution = []
    for i in range(k):
        exact_solution.append(dfs(graph, h_id, exact_solution))

    elapsed_time = time.time() - start_time
    print("global maxima: " + str(exact_solution))
    print("=> runtime (exact search): %0.3fs" % float(elapsed_time))
    """

    # TODO: tabu search
    print("\nTABU SEARCH:")
    start_time = time.time()
    solution = tabu_search(graph, h_id)
    print(f"solution: {solution}")
    elapsed_time = time.time() - start_time
    print("=> runtime (tabu search): %0.3fs" % float(elapsed_time))

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
    iterations = k * 5
    it = 0 # iteration counter

    if (DEBUG): print("k = " + str(k))

    # for i in range(iterations):
    while it < iterations or len(local_maxima) < k:
        initial_node = random_node(graph)

        if (DEBUG): print("\n-- search iteration " + str(it+1))
        if (DEBUG): print("initial node: " + str(initial_node))

        local_max, value = hill_climbing(graph, initial_node, heuristic_id, local_maxima)

        if (DEBUG): print("local max: " + str(local_max))
        if (DEBUG): print("value: " + str(value))
        local_maxima.add((local_max, value))

        it += 1

    solution = list(local_maxima)
    solution.sort(key = lambda x: x[1], reverse = True)
    solution = solution[:k]

    return solution

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

# tabu search
def tabu_search(graph, heuristic_id, tabu_size = 5):
    tabu_list = []
    initial_solution = random_node(graph) # ?
    print(f"initial solution: {initial_solution}")

    best_solution = initial_solution
    best_candidate = initial_solution
    tabu_list.append(initial_solution)
    max_it = 20
    it = 0

    while (it < max_it): # stopping condition?
        if (DEBUG): print(f"iteration {it}")
        s_neighborhood = list(graph.neighbors[best_candidate]) # ? build neighborhood
        best_candidate = s_neighborhood[0]
        if (DEBUG): print(f"best candidate: {best_candidate}")

        for candidate in s_neighborhood:
            candidate_value = heuristic_function(heuristic_id, graph, candidate)
            best_candidate_value = heuristic_function(heuristic_id, graph, best_candidate)

            if candidate not in tabu_list and candidate_value > best_candidate_value:
                best_candidate = candidate
                if (DEBUG): print(f"best candidate: {best_candidate}")
        
        best_candidate_value = heuristic_function(heuristic_id, graph, best_candidate)
        best_solution_value = heuristic_function(heuristic_id, graph, best_solution)

        if best_candidate_value > best_solution_value:
            best_solution = best_candidate
        
        if (DEBUG): print(f"best solution: {best_solution}")

        tabu_list.append(best_candidate)

        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)
        
        if (DEBUG): print(f"tabu list: {tabu_list}")

        it += 1

    return (best_solution, heuristic_function(heuristic_id, graph, best_solution))


main()