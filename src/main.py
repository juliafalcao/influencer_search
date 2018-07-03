# -*- coding: utf-8 -*-

from graph import *
from read_data import build_graph
import random
import time
import matplotlib.pyplot as plt

# heuristic function aliases
FRIENDS = Graph.neighbor_count
GROUPS = Graph.group_count

# to index (node, value) pairs clearly
NODE = 0
VALUE = 1

# whether to print debug messages or not
DEBUG = False

def run_tests(): # in construction
    k = 10
    global_maxima = [(1072, 28754), (363, 14641), (35661, 11281), (106, 10461), (482709, 9762), (663931, 8843), (929, 7917), (808, 6102), (27837, 5393), (108624, 4899)]
    rrhc_values = []
    
    for i in range(5):
        rrhc_solution, rrhc_runtime, _, _, _, _ = test(FRIENDS, k = k, output = False, dfs = False, ts = False)
        rrhc_values.append([pair[VALUE] for pair in rrhc_solution])

    rrhc_values = [pair[VALUE] for pair in rrhc_solution]
    dfs_values = [pair[VALUE] for pair in global_maxima]

    x_values = list(range(1,k+1))
    
    plt.plot(x_values, rrhc_values, linewidth = 2, color = "crimson", marker = "o", label = "RRHC")
    plt.plot(x_values, dfs_values, linewidth = 2, color = "darkturquoise", marker = "o", label = "global maxima")
    
    plt.xticks(x_values, ["v" + str(x) for x in x_values])
    plt.xlabel("Vértices encontrados")
    plt.ylabel("Valores")
    plt.title(f"Random-Restart Hill Climbing (k = {k})")
    plt.legend()
    plt.show()


"""
test function
receives the chosen heuristic and value of k
+ output: whether to print results
+ rrhc: whether to run random-restart hill climbing
+ dfs: whether to run exact depth-first search
+ ts: whether to run tabu search

"""
def test(heuristic, k, output = True, rrhc = True, dfs = True, ts = True):
    # build graph
    start_time = time.time()
    graph = build_graph(edges_filename = "../data/youtube/edges.txt", groups_filename = "../data/youtube/allcmty.txt")
    graph_runtime = time.time() - start_time
    if output: print("=> runtime (graph construction): %0.4fs" % float(graph_runtime))
    
    rrhc_solution = None; rrhc_runtime = None;
    dfs_solution = None; dfs_runtime = None;
    ts_solution = None; ts_runtime = None;

    if rrhc:
        # run random-restart hill climbing search
        if output: print("\nRANDOM-RESTART HILL CLIMBING:")
        start_time = time.time()
        rrhc_solution = search(graph, heuristic, k)
        rrhc_runtime = time.time() - start_time
        if output: print("solution: " + str(rrhc_solution))
        if output: print("=> runtime (random-restart hill climbing): %0.3fs" % float(rrhc_runtime))

    if dfs:
        # run exact depth-first search
        if output: print("\nEXACT DEPTH-FIRST SEARCH:")
        start_time = time.time()
        dfs_solution = []
        for i in range(k): dfs_solution.append(dfs(graph, heuristic, dfs_solution)) # TODO: optimize
        dfs_runtime = time.time() - start_time
        if output: print("global maxima: " + str(dfs_solution))
        if output: print("=> runtime (exact search): %0.3fs" % float(dfs_runtime))
    
    if ts:
        if output: print("\nTABU SEARCH:")
        start_time = time.time()
        ts_solution = tabu_search(graph, heuristic, k)
        ts_runtime = time.time() - start_time
        if output: print(f"solution: {ts_solution}")
        if output: print("=> runtime (tabu search): %0.3fs" % float(ts_runtime))


    return rrhc_solution, rrhc_runtime, dfs_solution, dfs_runtime, ts_solution, ts_runtime

"""
main search function
- randomly chooses initial nodes for all iterations
- runs hill climbing search iteratively
- checks when to stop iterations
"""
def search(graph, heuristic_function, k = 1):
    local_maxima = set() # all unique results found
    iterations = k * 5
    it = 0 # iteration counter

    if DEBUG: print("k = " + str(k))

    # for i in range(iterations):
    while it < iterations or len(local_maxima) < k:
        initial_node = random_node(graph)

        if DEBUG: print("\n-- search iteration " + str(it+1))
        if DEBUG: print("initial node: " + str(initial_node))

        local_max, value = hill_climbing(graph, initial_node, heuristic_function)

        if DEBUG: print("local max: " + str(local_max))
        if DEBUG: print("value: " + str(value))
        local_maxima.add((local_max, value))

        it += 1

    solution = list(local_maxima)
    solution.sort(key = lambda x: x[1], reverse = True)
    solution = solution[:k]

    return solution


"""
simple hill climbing search
"""
def hill_climbing(graph, initial_node, heuristic_function):
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
                count = heuristic_function(graph, n)

                if count >= max_count: # allows sideways moves
                    max_count = count
                    max_neighbor = n
        
        next, next_value = max_neighbor, max_count
        current_value = heuristic_function(graph, current)

        if next is None or next_value < current_value:
            return current, current_value # end of search

        current = next
        explored.add(next)


"""
get random node from the graph
"""
def random_node(graph):
    nodes = list(graph.neighbors.keys())
    return random.choice(nodes)


"""
exact depth-first search
returns the global maximum node, excluding the nodes in the excluded list
as a (node, value) pair
"""
def dfs(graph, heuristic_function, excluded):
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
            value = heuristic_function(graph, current)

            if value > max_value:
                max_value = value
                global_max = current

            visited.add(current)
            stack.extend(graph.neighbors[current] - visited)

    return (global_max, max_value)


"""
tabu search
"""
def tabu_search(graph, heuristic_function, k = 1, tabu_size = 5):
    tabu_list = []
    initial_solution = random_node(graph) # ?
    if DEBUG: print(f"initial solution: {initial_solution}")

    best_solutions = [] # list of (node, value) pairs
    best_solutions.append((initial_solution, heuristic_function(graph, initial_solution)))
    best_candidate = initial_solution
    tabu_list.append(initial_solution)
    max_it = 20
    it = 0

    while (it < max_it): # stopping condition?
        if DEBUG: print(f"iteration {it}")
        neighborhood = list(graph.neighbors[best_candidate]) # ? build neighborhood
        best_candidate = neighborhood[0]
        if DEBUG: print(f"best candidate: {best_candidate}")

        for candidate in neighborhood:
            candidate_value = heuristic_function(graph, candidate)

            if (candidate, candidate_value) not in best_solutions:
                best_candidate_value = heuristic_function(graph, best_candidate)

                if candidate not in tabu_list and candidate_value > best_candidate_value:
                    best_candidate = candidate
                    if DEBUG: print(f"best candidate: {best_candidate}")
        
        best_candidate_value = heuristic_function(graph, best_candidate)
        best_solution_value = heuristic_function(graph, best_solutions[0][VALUE])

        if best_candidate_value > best_solution_value:
            best_solutions.append((best_candidate, best_candidate_value))
            best_solutions.sort(key = lambda x: x[1], reverse = True)
        
        if DEBUG: print(f"best solutions: {best_solutions}")

        tabu_list.append(best_candidate)

        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)
        
        if DEBUG: print(f"tabu list: {tabu_list}")

        it += 1

    return best_solutions[:k]


run_tests()