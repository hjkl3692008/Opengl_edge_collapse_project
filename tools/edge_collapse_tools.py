import numpy as np
from tools import calculate_tools as ct


def remove_repeat_element(original_list):
    no_repeat_list = []
    for i in original_list:
        if i not in no_repeat_list:
            no_repeat_list.append(i)
    return no_repeat_list


class Vertex:

    def __init__(self, position=np.array([1, 1, 1]), vid=0, neighbor=None, face=None):
        if neighbor is None:
            neighbor = list()
        if face is None:
            face = list()
        self.face = face  # the triangles which contain this vector
        self.neighbor = neighbor  # neighbor vector of this vector
        self.vid = vid  # id of this vector
        self.position = position  # position of this vector
        calculate_edge_cost_at_vertex(self)

    def has_neighbor(self, test_vertex):
        for i, neighbor in enumerate(self.neighbor):
            if neighbor == test_vertex:
                return i
        return None

    def add_neighbor(self, neighbor_vertex):
        # if the input vector equal to itself, return
        if self == neighbor_vertex:
            return
        # add neighbor
        self.neighbor.append(neighbor_vertex)
        # remove repeat neighbor
        self.neighbor = remove_repeat_element(self.neighbor)

    def remove_neighbor(self, neighbor):
        # if this vector do not have the neighbor, return
        neighbor_index = self.has_neighbor(neighbor)
        if neighbor_index is None:
            return
        # if any face of this vector contain this neighbor, return
        for face in self.face:
            if face.has_vertex(neighbor) is not None:
                return
        # all check pass, remove this neighbor
        self.neighbor.remove(neighbor)

    # def replace_neighbor(self, old_n, new_n):
    #     self.remove_neighbor(old_n)
    #     self.add_neighbor(new_n)

    def add_face(self, triangle):
        self.face.append(triangle)
        # remove repeat neighbor
        self.face = remove_repeat_element(self.face)

    def remove_face(self, triangle):
        self.face.remove(triangle)

    def remove_self(self):
        assert len(self.face) == 0
        while len(self.neighbor) > 0:
            self.neighbor[0].remove_neighbor(self)
            self.remove_neighbor(self.neighbor[0])


class Triangle:
    def __init__(self, vertex1, vertex2, vertex3):
        self.vertex_list = [vertex1, vertex2, vertex3]
        self.calculate_normal()
        # add this triangle to all vertexes
        for vertex in self.vertex_list:
            vertex.add_face(self)
        # add neighbor to vertexes
        for vertex1 in self.vertex_list:
            for vertex2 in self.vertex_list:
                vertex1.add_neighbor(vertex2)

    def calculate_normal(self):
        self.normal = ct.normal_vector(self.vertex_list[1].position - self.vertex_list[0].position,
                                       self.vertex_list[2].position - self.vertex_list[1].position)

    def replace_vertex(self, old_vertex, new_vertex):
        # new vertex can not equal to old vertex
        assert old_vertex is not None and new_vertex is not None
        # this triangle contain the old vertex
        assert self.has_vertex(old_vertex) is not None
        # new vertex can not in this triangle
        assert new_vertex not in self.vertex_list

        vertex_index = self.has_vertex(old_vertex)
        if vertex_index is not None:
            self.vertex_list[vertex_index] = new_vertex
            old_vertex.remove_face(self)
            new_vertex.add_face(self)
            for vertex in self.vertex_list:
                old_vertex.remove_neighbor(vertex)
                vertex.remove_neighbor(old_vertex)
            for vertex in self.vertex_list:
                vertex.add_neighbor(new_vertex)
                new_vertex.add_neighbor(vertex)
            self.calculate_normal()

    def has_vertex(self, test_vertex):
        for i, vector in enumerate(self.vertex_list):
            if vector == test_vertex:
                return i
        return None

    def remove_self(self):
        # remove this triangle from vertex
        for vertex in self.vertex_list:
            vertex.remove_face(self)
        # remove neighbor relationship between vertexes
        num_vertexes = len(self.vertex_list)
        for i in range(num_vertexes):
            i2 = (i + 1) % num_vertexes
            self.vertex_list[i].remove_neighbor(self.vertex_list[i2])
            self.vertex_list[i2].remove_neighbor(self.vertex_list[i])
        # remove all vertexes in this triangle
        self.vertex_list = []


# the cost of edge fro u to v
def calculate_collapse_cost_between_two_vertex(vertex_u, vertex_v):
    # find triangle which contain edge uv
    uv_triangles = []
    for triangle in vertex_u.face:
        if triangle.has_vertex(vertex_v) is not None:
            uv_triangles.append(triangle)

    # find the triangle (contain u) most away from the triangles (contain uv)
    curvature = 0
    for i_tr in vertex_u.face:
        min_curve = 1
        for j_tr in uv_triangles:
            ij_curve = (1 - ct.dot(i_tr.normal, j_tr.normal)) / 2
            min_curve = min(min_curve, ij_curve)
        curvature = max(curvature, min_curve)

    edge_length = ct.edge_length(vertex_u.position, vertex_v.position)
    return edge_length * curvature


def calculate_edge_cost_at_vertex(vertex):
    # if there are not any neighbor:
    if len(vertex.neighbor) == 0:
        vertex.collapse_vertex = None
        vertex.collapsing_cost = 0.01
        return

    vertex.collapse_vertex = None
    vertex.collapsing_cost = float("inf")

    # find least cost edge
    for neighbor in vertex.neighbor:
        cost = calculate_collapse_cost_between_two_vertex(vertex, neighbor)
        if cost < vertex.collapsing_cost:
            vertex.collapse_vertex = neighbor
            vertex.collapsing_cost = cost


def calculate_all_cost(vertexes):
    for vertex in vertexes:
        calculate_edge_cost_at_vertex(vertex)


# move vertex u onto vertex v
def collapse(vertex_u, vertex_v, vertexes):
    # vertex u do not have any neighbor
    if vertex_v is None:
        vertexes.remove(vertex_u)
        vertex_u.remove_self()
        print("collapse u->v(None):", vertex_u.vid)
        return

    print("collapse u->v:", vertex_u.vid, vertex_v.vid)

    # copy u's neighbor
    temp_vertex_list = list(vertex_u.neighbor)
    temp_triangle_list = list(vertex_u.face)

    # remove u's face which contain edge uv
    # find all vertex which contain this face, and remove the face from those vertex
    for triangle in temp_triangle_list:
        if triangle.has_vertex(vertex_v) is not None:
            triangle.remove_self()
            # for vertex in triangle.vertex_list:
            #     vertex.face.remove(triangle)

    # replace u with v
    temp_triangle_list2 = list(vertex_u.face)
    for triangle in temp_triangle_list2:
        triangle.replace_vertex(vertex_u, vertex_v)

    # print("new v:", vertex_v.vid)
    # for i in range(len(vertex_v.face)):
    #     print(i, "triangle:")
    #     for vertex in vertex_v.face[i].vertex_list:
    #         print(vertex.vid)

    # delete u
    vertexes.remove(vertex_u)
    vertex_u.remove_self()

    # re-calculate the cost of u's neighbor
    for vertex in temp_vertex_list:
        calculate_edge_cost_at_vertex(vertex)


def find_vertex_with_minimum_cost_edge(vertexes):
    min_vertex = vertexes[0]
    for vertex in vertexes:
        if vertex.collapsing_cost < min_vertex.collapsing_cost:
            min_vertex = vertex
    return min_vertex


# order vertexes and triangles by permutation
def order_by_permutation(vertexes, triangles, permutation):
    temp_vertex_array = vertexes.copy()
    for i in range(len(vertexes)):
        vertexes[permutation[i]] = temp_vertex_array[i]

    # triangles_indices = np.zeros((len(triangles), 3), dtype=np.int)
    # normal = np.zeros((len(triangles), 3))
    # for i in range(len(triangles)):
    #     for j in range(len(triangles[i].vertex_list)):
    #         triangles_indices[i, j] = permutation[triangles[i].vertex_list[j].vid]
    #     normal[i] = triangles[i].normal

    for i in range(triangles.shape[0]):
        for j in range(triangles.shape[1]):
            triangles[i, j] = permutation[triangles[i, j]]

    # todo:// re-calculate texture uv?

    return vertexes, triangles


def check_repeat_vertex_in_triangles(triangles):
    for triangle in triangles:
        v1 = triangle.vertex_list[0]
        v2 = triangle.vertex_list[1]
        v3 = triangle.vertex_list[2]
        if v1.vid == v2.vid or v1.vid == v2.vid or v2.vid == v3.vid:
            print("this triangle has repeated vertex")


# calculate collapse order
def prepare_collapse(vertexes_positions, triangles_indices):
    vertexes = []
    vid = 0
    for position in vertexes_positions:
        vertexes.append(Vertex(position=position, vid=vid))
        vid = vid + 1

    triangles = []
    for tr in triangles_indices:
        vertex1 = vertexes[tr[0]]
        vertex2 = vertexes[tr[1]]
        vertex3 = vertexes[tr[2]]
        triangles.append(Triangle(vertex1, vertex2, vertex3))

    calculate_all_cost(vertexes)

    # check_repeat_vertex_in_triangles(triangles)

    permutation = np.zeros(len(vertexes), dtype=np.int)
    collapse_map = np.zeros(len(vertexes), dtype=np.int)
    while len(vertexes) > 0:
        min_vertex = find_vertex_with_minimum_cost_edge(vertexes)
        vertexes_length = len(vertexes)
        # u's order
        permutation[min_vertex.vid] = vertexes_length - 1
        # v's order
        if min_vertex.collapse_vertex is not None:
            collapse_map[vertexes_length - 1] = min_vertex.collapse_vertex.vid
        else:
            collapse_map[vertexes_length - 1] = -1
        # collapse uv, u is point need removed, v is point remained
        collapse(min_vertex, min_vertex.collapse_vertex, vertexes)

    # reorder collapse_map by permutation
    # :reorder v by collapse order
    for i in range(len(collapse_map)):
        if collapse_map[i] == -1:
            collapse_map[i] = 0
        else:
            collapse_map[i] = permutation[collapse_map[i]]

    vertexes_positions, triangles_indices = order_by_permutation(vertexes_positions, triangles_indices,
                                                                 permutation)

    return vertexes_positions, triangles_indices, collapse_map, permutation


if __name__ == '__main__':
    v1 = Vertex(np.array([1, 1, 1]), 1)
    v2 = Vertex(np.array([1, 2, 2]), 2)
    v3 = Vertex(np.array([4, 1, 1]), 3)
    v4 = Vertex(np.array([4, 3, 9]), 4)  # v
    v5 = Vertex(np.array([5, 5, 3]), 5)  # u
    vertexes = [v1, v2, v3, v4, v5]
    tr1 = Triangle(v1, v2, v5)
    tr2 = Triangle(v2, v3, v5)
    tr3 = Triangle(v3, v4, v5)
    tr4 = Triangle(v1, v4, v5)
    collapse(v5, v4, vertexes)
    pass
