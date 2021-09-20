from DirectedGraph import create_random_graph


def find_accessible_vertices_backwards(graph, end_vertex):
    if end_vertex not in graph.parse_vertices():
        raise ValueError("The end vertex is not in the graph.")

    visited = []
    queue = []
    next_vertex = {}
    distance_to_end = {}

    queue.append(end_vertex)
    visited.append(end_vertex)
    distance_to_end[end_vertex] = 0
    while len(queue) > 0:
        y = queue[0]
        queue = queue[1:]
        for edge in graph.parse_inbound_edges(y):
            if edge.a_id not in visited:
                visited.append(edge.a_id)
                queue.append(edge.a_id)
                distance_to_end[edge.a_id] = distance_to_end[y] + 1
                next_vertex[edge.a_id] = y

    return next_vertex


def find_minimum_length_path(graph, start_vertex, end_vertex):
    next_vertex = find_accessible_vertices_backwards(graph, end_vertex)

    if start_vertex not in next_vertex.keys():
        raise ValueError("There is no path from " + str(start_vertex) + " to " + str(end_vertex))

    path = [start_vertex]
    previous_vertex = start_vertex
    reached_end = False
    while not reached_end:
        path.append(next_vertex[previous_vertex])
        previous_vertex = next_vertex[previous_vertex]
        if path[-1] == end_vertex:
            reached_end = True

    return path


def main():
    random_graph = create_random_graph(8, 16)

    print("THE GRAPH:")
    for vertex in random_graph.parse_vertices():
        for edge in random_graph.parse_edges(vertex):
            print(edge)

    print("\n")

    # next_vertex = find_accessible_vertices_backwards(random_graph, 4)
    # for node in next_vertex.keys():
    #     print(str(node) + " -> " + str(next_vertex[node]))

    try:
        path = find_minimum_length_path(random_graph, 1, 4)
        print("The lowest length path is:")
        string_path = ""
        for vertex in path:
            string_path = string_path + str(vertex) + " -> "
        string_path = string_path[:-4]
        print(string_path)
    except ValueError as error_message:
        print(error_message)


main()
