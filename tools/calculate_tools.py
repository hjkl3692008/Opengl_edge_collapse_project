import numpy as np
from scipy.spatial import distance


# normalize vector
def unit_vector(v):
    length = np.linalg.norm(v)
    if length == 0:
        print("there are zero")
    uv = v / length
    return uv


# normalize vectors
def unit_vectors(vs):
    for i in range(0, vs.shape[0]):
        vs[i] = unit_vector(vs[i])
    return vs


# normal vector of v1, v2
def normal_vector(v1, v2):
    nv = np.cross(v1, v2)
    nv = unit_vector(nv)
    return nv


# calculate all normals
def cal_all_normals(points, polygons):
    # [0] save how many polygons the vertex involves, [1:4] save normal of this vertex
    normals = np.zeros((points.shape[0], 4))
    for i in range(0, polygons.shape[0]):
        v1_index = polygons[i, 1] - 1
        v2_index = polygons[i, 2] - 1
        v3_index = polygons[i, 3] - 1
        v1 = points[v1_index]
        v2 = points[v2_index]
        v3 = points[v3_index]
        # normal of this triangle
        normal = normal_vector(v2 - v1, v3 - v2)
        normal = np.hstack((1, normal))
        for j in range(1, polygons[i, 0] + 1):
            v_index = int(polygons[i, j]) - 1
            normals[v_index] = normals[v_index] + normal
    # mean of normal
    for i in range(0, normals.shape[0]):
        num = normals[i, 0]
        normals[i] = normals[i] / num
    # delete counts
    normals = normals[:, 1:4]
    # unit normals
    normals = unit_vectors(normals)
    return normals


# reflect direction
def reflect(in_direction, normal, is_unit=True):
    reflection = 2 * normal * np.dot(normal, in_direction) - in_direction
    if is_unit:
        reflection = unit_vector(reflection)
    return reflection


def edge_length(v1_position, v2_position, dim=2):
    return distance.minkowski(v1_position, v2_position, dim)


def dot(vector1, vector2):
    return np.dot(vector1, vector2)


def norm(x):
    return np.linalg.norm(x)
