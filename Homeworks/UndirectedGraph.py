
import copy
from random import randint

def read_graph(graph, name_of_file):
    file = open(name_of_file, "rt")
    content = file.readlines()
    file.close()
    first_line = content[0]
    first_line = first_line.split(" ")

    number_of_vertices = int(first_line[0])
    number_of_edges = int(first_line[1][:-1])

    for vertex in range(0, number_of_vertices):
        new_vertex = Vertex(graph.current_vertex_id)
        graph.current_vertex_id += 1
        graph.edges[new_vertex.id] = []

    for line in range(1, number_of_edges + 1):
        data = content[line].split(" ")
        vertex_a = Vertex(int(data[0]))
        vertex_b = Vertex(int(data[1]))
        cost = int(data[2][:-1])

        graph.add_edge(vertex_a.id, vertex_b.id, cost)


def write_graph(graph, name_of_file):
    file = open(name_of_file, 'wt')

    # the first line
    line = str(graph.number_of_vertices) + ' ' + str(graph.number_of_edges)
    file.write(line)
    file.write('\n')

    # the edges
    for vertex in graph.edges.keys():
        for edge in graph.edges[vertex]:
            line = str(edge)
            file.write(line)
            file.write('\n')

    file.close()


def create_random_graph(number_of_vertices, number_of_edges):
    if number_of_vertices <= 0:
        raise ValueError("The number of vertices must be positive.")
    if number_of_edges < 0:
        raise ValueError("The number of edges must be >= 0.")

    if number_of_edges > number_of_vertices**2:
        raise ValueError("The number of edges cannot be greater than the number of vertices squared.")

    graph = UndirectedGraph()
    for vertex in range(0, number_of_vertices):
        new_vertex = Vertex(graph.current_vertex_id)
        graph.current_vertex_id += 1
        graph.edges[new_vertex.id] = []

    while graph.number_of_edges < number_of_edges:
        a = randint(0, number_of_vertices-1)
        b = randint(0, number_of_vertices-1)
        edge_cost = randint(-100, 100)

        if not graph.is_edge_from_to(a, b):
            graph.add_edge(a, b, edge_cost)

    return graph


class Edge:
    def __init__(self, edge_id, vertex_b_id, vertex_a_id, cost):
        self.__edge_id = edge_id
        self.__a = vertex_b_id
        self.__b = vertex_a_id
        self.__cost = cost

    @property
    def edge_id(self):
        return self.__edge_id

    @property
    def a_id(self):
        return self.__a

    @property
    def b_id(self):
        return self.__b

    @property
    def cost(self):
        return self.__cost

    @cost.setter
    def cost(self, value):
        self.__cost = value

    def __str__(self):
        return str(self.a_id) + " -> " + str(self.b_id) + "   cost " + str(self.cost)


class Vertex:
    def __init__(self, _id):
        self.__vertex_id = _id

    @property
    def id(self):
        return self.__vertex_id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(repr(self))


class UndirectedGraph:
    def __init__(self):
        self.__number_of_edges = 0
        self.__edges = {}
        # self.__inbound_edges = {}
        self.__current_edge_id = 1
        self.__current_vertex_id = 0
        self._ham_path_cost = 0
        self._starting_vertex = 0
        self._ham_path_vertices = []
        self._visited = []

    @property
    def number_of_edges(self):
        return self.__number_of_edges

    @number_of_edges.setter
    def number_of_edges(self, value):
        self.__number_of_edges = value

    @property
    def edges(self):
        return self.__edges

    @property
    def current_edge_id(self):
        return self.__current_edge_id

    @current_edge_id.setter
    def current_edge_id(self, value):
        self.__current_edge_id = value

    @property
    def current_vertex_id(self):
        return self.__current_vertex_id

    @current_vertex_id.setter
    def current_vertex_id(self, value):
        self.__current_vertex_id = value

    @property
    def number_of_vertices(self):
        return len(self.edges)

    def parse_vertices(self):
        # for vertex in self.outbound_neighbours.keys():
        #     yield vertex
        return self.edges.keys()

    def parse_edges(self, vertex_id):
        if vertex_id not in self.edges.keys():
            raise ValueError("The given vertex does not exist.")
        for edge in self.edges[vertex_id]:
            yield edge

    def is_edge_from_to(self, vertex_a_id, vertex_b_id):
        if vertex_a_id not in self.edges.keys() or vertex_b_id not in self.edges.keys():
            raise ValueError("The given vertex does not exist.")
        for edge in self.edges[vertex_a_id]:
            if edge.b_id == vertex_b_id:
                return edge.edge_id

        return 0

    def get_degree(self, vertex_id):
        if vertex_id not in self.edges.keys():
            raise ValueError("The given vertex does not exist.")

        in_degree = 0
        for edge in self.edges[vertex_id]:
            in_degree += 1

        return in_degree

    def get_endpoints_of_an_edge(self, edge_id):
        a_and_b = []
        for vertex in self.edges.keys():
            for edge in self.edges[vertex]:
                if edge.edge_id == edge_id:
                    a_and_b.append(edge.a_id)
                    a_and_b.append(edge.b_id)
                    return a_and_b

        raise ValueError("There is no edge with the given id.")

    def get_cost_of_edge(self, vertex_a_id, vertex_b_id):
        if vertex_a_id not in self.edges.keys() or vertex_b_id not in self.edges.keys():
            raise ValueError("The given vertex does not exist.")

        if vertex_a_id == vertex_b_id:
            return 0

        for edge in self.edges[vertex_a_id]:
            if edge.b_id == vertex_b_id:
                return edge.cost

        raise ValueError("There is no edge between the given vertices.")


    def update_cost_of_edge(self, vertex_a_id, vertex_b_id, new_value):
        if vertex_a_id not in self.edges.keys() or vertex_b_id not in self.edges.keys():
            raise ValueError("The given vertex does not exist.")

        for edge in self.edges[vertex_a_id]:
            if edge.b_id == vertex_b_id:
                edge.cost = new_value
                return

    def add_edge(self, vertex_a_id, vertex_b_id, edge_cost):
        if vertex_a_id not in self.edges.keys():
            raise ValueError("The source vertex does not exist.")

        if vertex_b_id not in self.edges.keys():
            raise ValueError("The target vertex does not exist.")

        if self.is_edge_from_to(vertex_a_id, vertex_b_id):
            raise ValueError("There already exists an edge between these vertices.")

        new_edge = Edge(self.current_edge_id, vertex_a_id, vertex_b_id, edge_cost)

        self.edges[vertex_a_id].append(new_edge)
        self.edges[vertex_b_id].append(new_edge)
        self.current_edge_id += 1
        self.number_of_edges += 1

    def remove_edge(self, vertex_a_id, vertex_b_id):
        if vertex_a_id not in self.edges.keys() or vertex_b_id not in self.edges.keys():
            raise ValueError("The given vertex does not exist.")

        for edge in self.edges[vertex_a_id]:
            if edge.b_id == vertex_b_id:
                self.edges[vertex_a_id].remove(edge)
                break

        for edge in self.edges[vertex_b_id]:
            if edge.a_id == vertex_a_id:
                self.edges[vertex_b_id].remove(edge)
                break

    def add_vertex(self):
        new_vertex = Vertex(self.current_vertex_id)
        self.current_vertex_id += 1
        self.edges[new_vertex.id] = []

    def remove_vertex(self, vertex_id):
        if vertex_id not in self.edges.keys():
            raise ValueError("The vertex with the given id does not exist.")

        # remove its edges
        del self.edges[vertex_id]

        # delete its inbound edges coming out from other vertices
        for vertex in self.edges.keys():
            for edge in self.edges[vertex]:
                if edge.b_id == vertex_id:
                    self.edges[vertex].remove(edge)

    def copy(self):
        copy_of_graph = copy.deepcopy(self)
        return copy_of_graph

    def dfs_nearest_neighbor(self, source_vertex, cycle_length):
        self._visited[source_vertex] = True
        sorted_outbound_neighbours = self.edges[source_vertex]
        sorted_outbound_neighbours = sorted(sorted_outbound_neighbours, key=lambda edge1: edge1.cost)
        found_original_vertex = False

        for edge in sorted_outbound_neighbours:
            if edge.a_id == source_vertex:
                neighbor = edge.b_id
            else:
                neighbor = edge.a_id

            if neighbor == self._starting_vertex and cycle_length == self.number_of_vertices - 1:
                self._ham_path_vertices.append(source_vertex)
                self._ham_path_cost += edge.cost
                return True
            elif not self._visited[neighbor]:
                found_original_vertex = self.dfs_nearest_neighbor(neighbor, cycle_length+1)
                if found_original_vertex:
                    self._ham_path_vertices.append(source_vertex)
                    self._ham_path_cost += edge.cost
                    return True

        self._visited[source_vertex] = False
        return found_original_vertex

    def approximate_tsp_nearest_neighbor(self):
        self._starting_vertex = 0
        self._ham_path_cost = 0
        self._visited.clear()
        for i in range(0, self.number_of_vertices):
            self._visited.append(False)

        self._ham_path_vertices.clear()
        self.dfs_nearest_neighbor(self._starting_vertex, 0)
        self._ham_path_vertices.insert(0, self._starting_vertex)

    def get_ham_path_vertices(self):
        return self._ham_path_vertices

    def get_ham_path_cost(self):
        return self._ham_path_cost