from DirectedGraph import Graph, read_graph
from collections import deque

# 3. Write a program that, given a graph with costs, does the following:
#
# verify if the corresponding graph is a DAG and performs a topological sorting of the activities using the algorithm
# based on depth-first traversal (Tarjan's algorithm);

# if it is a DAG, finds a highest cost path between two given vertices, in O(m+n).


def find_maximum_cost_path(graph, sorted_vertices, source, destination):
    costs = [0] * graph.number_of_vertices
    i = 0
    predecessors_on_maximum_path = {}

    while i < len(sorted_vertices) and sorted_vertices[i] != source:
        i += 1

    while i < len(sorted_vertices) and sorted_vertices[i] != destination:

        vertex = sorted_vertices[i]

        for current in graph.parse_vertices():
            try:
                cost_of_current_edge = graph.get_cost_of_edge(vertex, current)

                new_cost = costs[vertex] + cost_of_current_edge
                if new_cost > costs[current]:
                    costs[current] = new_cost
                    predecessors_on_maximum_path[current] = [vertex, new_cost]
            except ValueError as ve:
                pass
        i += 1

    if destination not in predecessors_on_maximum_path.keys():
        return -1

    # build the path
    max_cost = predecessors_on_maximum_path[destination][1]

    path = [destination]
    current = destination
    reached_end = False
    while not reached_end:
        path.insert(0, predecessors_on_maximum_path[current][0])
        current = predecessors_on_maximum_path[current][0]
        if path[0] == source:
            reached_end = True

    path.insert(0, max_cost)
    return path




def sub_topo_sort(graph, vertex, sorted_vertices, fully_processed, in_process):
    in_process.append(vertex)
    for edge in graph.parse_inbound_edges(vertex):
        predecessor = edge.a_id
        if predecessor in in_process:
            return False
        elif predecessor not in fully_processed:
            ok = sub_topo_sort(graph, predecessor, sorted_vertices, fully_processed, in_process)
            if not ok:
                return False

    in_process.remove(vertex)
    sorted_vertices.append(vertex)
    fully_processed.append(vertex)
    return True


def sort_topologically(graph):
    sorted_vertices = []
    fully_processed = []
    in_process = []
    for vertex in graph.parse_vertices():
        if vertex not in fully_processed:
            ok = sub_topo_sort(graph, vertex, sorted_vertices, fully_processed, in_process)
            if not ok:
                raise TypeError("The graph contains cycles.")

    return sorted_vertices


def main():
    graph = Graph()
    read_graph(graph, "hw4_data")
    try:
        sorted_vertices = sort_topologically(graph)
        print("One topological sorting of the graph is:")
        print(sorted_vertices)
        print("\n")

        path = find_maximum_cost_path(graph, sorted_vertices, 0, 2)
        # print(path)
        cost_of_path = path[0]
        print("The maximum cost path has the cost", cost_of_path)
        path = path[1:]
        print("and the path is", path)
    except TypeError as error_message:
        print(error_message)


main()
