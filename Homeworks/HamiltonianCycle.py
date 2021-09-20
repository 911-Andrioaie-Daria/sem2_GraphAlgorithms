# 10. Given an undirected graph with costs, find a Hamiltonian cycle of low cost (approximate TSP) by using
# the heuristic of taking, from the current vertex, the edge of minimum cost that do not close a cycle of length
# lower than n.

from UndirectedGraph import read_graph, UndirectedGraph


def main():
    graph = UndirectedGraph()
    read_graph(graph, "hm5_data")
    graph.approximate_tsp_nearest_neighbor()

    ham_path_vertices = graph.get_ham_path_vertices()

    if len(ham_path_vertices) == 0:
        print("No cycle found (perhaps the graph is acyclic ?)\n")
        return

    print("Hamiltonian cycle cost: " + str(graph.get_ham_path_cost()))
    path = ""
    for vertex in graph.get_ham_path_vertices():
        path += str(vertex) + " -> "
    path = path[:-4]
    print(path)


main()
