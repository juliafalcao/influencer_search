from ego_init import get_ego_graphs
from graph import *
import random


def main():
    ego_graphs = get_ego_graphs()

    print("global max: " + str(global_max(ego_graphs[107])))
    print(search(ego_graphs[107], next_node, 5))


# main random-restart hill climbing search function
def search(graph, next_node, k = 1):
    # decides initial node
    # runs search iteratively
    # checks when to stop iterations

    nodes = list(graph.neighbors.keys())
    influencers = []

    while (len(influencers) < k):
        initial_node = random.choice(nodes)
        print("k = " + str(k))
        print("initial node: " + str(initial_node) + "\n")
        local_max = hill_climbing(graph, initial_node, next_node)
        influencers.append(local_max)
    
    return influencers
        



def next_node(graph, current_node):
    neighbors = graph.neighbors[current_node]
    
    max_friend_count = 0
    max_neighbor = None
    
    for n in neighbors:
        friend_count = graph.neighbor_count(n)

        if friend_count > max_friend_count:
            max_friend_count = friend_count
            max_neighbor = n

    return max_neighbor

def global_max(graph):
    max_neighbors = 0
    global_max = None

    for node in graph.neighbors:
        neighbor_count = graph.neighbor_count(node)
        if neighbor_count > max_neighbors:
            max_neighbors = neighbor_count
            global_max = node

    return global_max



# hill climbing search
# next is the function that returns the next node to visit (the one with the highest heuristic value)
def hill_climbing(graph, initial_node, next_node):
    if initial_node not in graph.neighbors:
        print("ERRO: Initial node given is not in graph.", file = sys.stderr)
        return

    current = initial_node
    
    while True:
        # !!
        next = next_node(graph, current)

        if graph.neighbor_count(next) < graph.neighbor_count(current):
            return current # fim da busca

        current = next

main()


