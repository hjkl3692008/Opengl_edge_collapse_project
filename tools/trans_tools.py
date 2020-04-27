import numpy as np


# polygon2triangle
def polygon2triangle(polygons):
    triangles = None
    for polygon in polygons:
        vertex_num = polygon[0]
        if vertex_num == 3:
            # this is a triangle
            triangle = np.array(polygon[1:4], dtype='int32')
            if triangles is None:
                triangles = triangle
            else:
                triangles = np.vstack((triangles, triangle))
        else:
            # not a triangle
            for i in range(2, vertex_num):
                f_vertex = polygon[i - 1]
                s_vertex = polygon[i]
                t_vertex = polygon[vertex_num]
                triangle = np.array([f_vertex, s_vertex, t_vertex], dtype='int32')
                if triangles is None:
                    triangles = triangle
                else:
                    triangles = np.vstack((triangles, triangle))
    # inverse direction!!!
    triangles = triangles[:, [2, 1, 0]]
    # index = index - 1, because index start with 0
    triangles = triangles - 1
    return triangles
