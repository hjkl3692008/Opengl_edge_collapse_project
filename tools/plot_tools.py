from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import glm

import numpy as np
import random

import tools.calculate_tools as ct
import tools.trans_tools as trans_t


RED_COLOR = np.array([1.0, 0.0, 0.0, 1.0])
BLUE_COLOR = np.array([0.0, 0.0, 1.0, 1.0])
GREEN_COLOR = np.array([0.0, 1.0, 0.0, 1.0])
YELLOW_COLOR = np.array([1.0, 1.0, 0.0, 1.0])

COLOR_DICT = {1: RED_COLOR, 2: BLUE_COLOR, 3: GREEN_COLOR, 4: YELLOW_COLOR}

POLYGON_AND_LINE = 'BOTH'


class Vertex:
    position = None
    color = None

    def __init__(self, position, color=RED_COLOR):
        self.position = position
        self.color = color


def plot_one_polygon(polygon):
    for vertex in polygon:
        color = vertex.color
        glColor4f(color[0], color[1], color[2], color[3])
        position = vertex.position
        glVertex3f(position[0], position[1], position[2])


def plot_polygons(points, polygons, is_random_color):
    for i in range(polygons.shape[0]):
        polygon = polygons[i]
        glBegin(GL_POLYGON)
        vertexes = []
        vertex_num = int(polygon[0])
        # constant color
        num = (i % 4) + 1
        for vertex_index in polygon[1: 1+vertex_num]:
            position = points[int(vertex_index)-1]
            v = Vertex(position)
            if is_random_color:
                # random color, Flat model -> Smooth model
                # num = random.randint(1, 4)
                v.color = COLOR_DICT[num]
            vertexes.append(v)
        plot_one_polygon(vertexes)
        glEnd()


def plot_one_line(vertex1, vertex2):
    color = vertex1.color
    glColor4f(color[0], color[1], color[2], color[3])
    position1 = vertex1.position
    position2 = vertex2.position
    glVertex3f(position1[0], position1[1], position1[2])
    glVertex3f(position2[0], position2[1], position2[2])


def plot_lines(points, polygons):
    for polygon in polygons:
        vertex_num = int(polygon[0])
        for i in range(1, 1+vertex_num):
            glBegin(GL_LINES)
            position1 = points[int(polygon[i]) - 1]
            v1 = Vertex(position1)
            position2 = None
            if i == vertex_num:
                position2 = points[int(polygon[1]) - 1]
            else:
                position2 = points[int(polygon[i+1]) - 1]
            v2 = Vertex(position2)
            plot_one_line(v1, v2)
            glEnd()


def plot_one_triangle(vertex1, vertex2, vertex3):
    color = vertex1.color
    glColor4f(color[0], color[1], color[2], color[3])
    position1 = vertex1.position
    position2 = vertex2.position
    position3 = vertex3.position
    glVertex3f(position1[0], position1[1], position1[2])
    glVertex3f(position2[0], position2[1], position2[2])
    glVertex3f(position3[0], position3[1], position3[2])


def plot_triangles(points, polygons):
    triangles = trans_t.polygon2triangle(polygons)
    for i in range(0, triangles.shape[0]):
        triangle = triangles[i]
        glBegin(GL_TRIANGLES)
        position1 = points[int(triangle[0]) - 1]
        position2 = points[int(triangle[1]) - 1]
        position3 = points[int(triangle[2]) - 1]
        v1 = Vertex(position1)
        num = (i % 4) + 1
        v1.color = COLOR_DICT[num]
        v2 = Vertex(position2)
        v3 = Vertex(position3)
        plot_one_triangle(v1, v2, v3)
        glEnd()


def plot_cow(gl_type, points, polygons, is_random_color=True, light=None, camera=None):

    if gl_type == GL_POLYGON:  # polygon mode
        plot_polygons(points, polygons, is_random_color)
    elif gl_type == GL_LINES:  # line mode
        plot_lines(points, polygons)
    elif gl_type == POLYGON_AND_LINE:  # polygon & line
        plot_polygons(points, polygons, is_random_color)
        plot_lines(points, polygons)
    elif gl_type == GL_TRIANGLES:  # triangles mode
        plot_triangles(points, polygons)


# def infinity_light(normal, light, ca):
#
#     light_direction = light.LIGHT_DIRECTION
#     view_direction = ca.N
#     reflect_light_direction = ct.reflect(light_direction, normal)
#
#     light_intensity = light.INTENSITY
#
#     # ambient
#     ambient = np.maximum(np.zeros(3), light_intensity * cow.K_AMBIENT)
#     # diffuse
#     diffuse = np.maximum(np.zeros(3), light_intensity * cow.K_DIFFUSE * np.dot(normal, light_direction))
#
#     # specular
#     temp = np.maximum(0.0, np.dot(reflect_light_direction, view_direction))
#     if diffuse[0] == 0.0:
#         temp = 0.0
#     else:
#         temp = np.pow(temp, cow.SHININESS_DEGREE)
#     specular = np.maximum(np.zeros(3), light_intensity * cow.K_SPECULAR * temp)
#
#     rgb = np.minimum(np.ones(3), ambient + diffuse + specular)
#     color = np.array([rgb[0], rgb[1], rgb[2], 1.0])
#
#     return color
