import numpy as np
import glm

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from tools import file_tools as ft
from tools import trans_tools as tt
from tools import calculate_tools as ct
from tools import edge_collapse_tools as et
from tools import plot_tools as pt

from model.animator import Animator

class Cow(object):

    def __init__(self, animator=Animator(step=20,final_fraction=0.1)):
        self.animator = animator

    def load_data(self):
        # load original data
        head, vertexes, self.indices = ft.load_cow()
        # trans data format
        indices = tt.polygon2triangle(self.indices)
        # prepare collapse
        self.vertexes, self.triangles, self.collapse_map, self.permutation = et.prepare_collapse(vertexes, indices)
        self.max_point = vertexes.shape[0]

    def mapping(self, index, max_point):
        if max_point <= 0:
            return 0
        while index >= max_point:
            index = self.collapse_map[index]
        return index

    def test_rendering(self):
        pt.plot_cow(gl_type=GL_TRIANGLES, points=self.vertexes, polygons=self.indices)

    def time_function(self, timer):
        self.max_point = (1 - self.animator.iterate())*self.vertexes.shape[0]
        self.update_f()
        glutTimerFunc(self.animator.each_step_time, self.time_function, timer)

    def rendering(self):

        # draw triangles
        for triangle in self.triangles:
            p0 = self.mapping(triangle[0], self.max_point)
            p1 = self.mapping(triangle[1], self.max_point)
            p2 = self.mapping(triangle[2], self.max_point)

            if p0 == p1 or p1 == p2 or p2 == p0:
                continue

            v0 = self.vertexes[p0]
            v1 = self.vertexes[p1]
            v2 = self.vertexes[p2]

            # if (v0 == v1).any() or (v1 == v2).any() or (v2 == v0).any():
            #     continue

            mode = GL_TRIANGLES
            glBegin(mode)
            normal = ct.normal_vector(v1 - v0, v2 - v1)
            if ct.norm(normal) > 0:
                glNormal3fv(normal)
            # glColor4f(0.0, 1.0, 0.0, 1.0)
            # glVertex3f(v0[0], v0[1], v0[2])
            # glVertex3f(v1[0], v1[1], v1[2])
            # glVertex3f(v2[0], v2[1], v2[2])
            glVertex3fv(v0)
            glVertex3fv(v1)
            glVertex3fv(v2)
            glEnd()
