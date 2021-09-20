from DirectedGraph import Graph, read_graph


def has_negative_cycles(graph, src):
    infinity = float('inf')
    v = graph.number_of_vertices
    dist = [infinity for _ in range(v)]
    dist[src] = 0

    for i in range(1, v):
        for vertex in graph.parse_vertices():
            for edge in graph.parse_edges(vertex):
                cost_of_edge = graph.get_cost_of_edge(vertex, edge.b_id)
                if dist[vertex] != infinity and dist[vertex] + cost_of_edge < dist[edge.b_id]:
                    dist[edge.b_id] = dist[vertex] + cost_of_edge

    for vertex in graph.parse_vertices():
        for edge in graph.parse_edges(vertex):
            cost_of_edge = graph.get_cost_of_edge(vertex, edge.b_id)
            if dist[vertex] != infinity and dist[vertex] + cost_of_edge < dist[edge.b_id]:
                return True
    return False


def find_minimum_cost_walk(start_vertex, end_vertex, graph):
    if start_vertex not in graph.parse_vertices():
        raise ValueError("The end vertex is not in the graph.")

    if end_vertex not in graph.parse_vertices():
        raise ValueError("The end vertex is not in the graph.")

    infinity = float('inf')
    v = graph.number_of_vertices

    # build the matrix dist[k][x] = the cost of the lowest cost walk from s to x and of length equal to k,
    # where s is the starting vertex.

    dist = [[infinity for _ in range(v)] for _ in range(v + 1)]
    dist[0][start_vertex] = 0

    previous = [[infinity for _ in range(v)] for _ in range(v)]

    for length in range(1, v):
        for vertex in graph.parse_vertices():
            if dist[length - 1][vertex] != infinity:
                for edge in graph.parse_edges(vertex):
                    if dist[length][edge.b_id] > dist[length - 1][vertex] + graph.get_cost_of_edge(vertex,
                                                                                                   edge.b_id):
                        dist[length][edge.b_id] = dist[length - 1][vertex] + graph.get_cost_of_edge(vertex,
                                                                                                    edge.b_id)
                        previous[length][edge.b_id] = vertex

    minimum_cost = infinity
    minimum_length = 0
    for length in range(1, v):
        if dist[length][end_vertex] < minimum_cost:
            minimum_cost = dist[length][end_vertex]
            minimum_length = length

    walk = [end_vertex]
    current = end_vertex

    for length in range(minimum_length, 0, -1):
        walk.insert(0, previous[length][current])
        current = previous[length][current]

    walk.append(minimum_cost)

    return walk


def main():
    graph = Graph()
    read_graph(graph, "input_data.txt")

    if has_negative_cycles(graph, 0):
        print("The graph has negative cycles.")
    else:
        try:
            walk = find_minimum_cost_walk(0, 1, graph)
            cost = walk[-1]
            walk = walk[:-1]
            print("The lowest cost walk is:")
            string_path = ""
            for vertex in walk:
                string_path = string_path + str(vertex) + " -> "
            string_path = string_path[:-4]
            print(string_path)
            print("Cost: " + str(cost))
        except ValueError as error_message:
            print(error_message)

main()
