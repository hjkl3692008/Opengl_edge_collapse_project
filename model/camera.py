import numpy as np
import glm


class Camera:
    EYE = None  # camera position
    PREF = None  # view direction
    vv = None  # the positive direction of Y-axis

    N = None  # Z-axis of camera space
    U = None  # X-axis of camera space
    EYE_UP = None  # Y-axis of camera space

    # view frustum
    d = None  # near
    half_h = None  # 1/2 high
    f = None  # far
    fov = None  # Field of View

    width = None
    height = None

    VIEW = None
    LOOK_AT = None

    # project matrix
    ProjectionMatrix = None
    ViewMatrix = None

    MVP = None

    def __init__(self, position=np.array([0.0, 0.0, 10.0]), pref=np.array([0.0, 0.0, -1.0]),
                 vv=np.array([0.0, 1.0, 0.0]), d=4.0, width=500, height=4.0, f=100.0):
        # if use shader, remember change d->0.1, height->500
        self.EYE = position
        self.PREF = pref
        self.vv = vv
        self.N = (self.PREF - self.EYE) / np.linalg.norm(self.PREF - self.EYE)
        self.U = np.cross(self.N, self.vv) / np.linalg.norm(np.cross(self.N, self.vv))
        self.EYE_UP = np.cross(self.U, self.N)
        self.d = d
        self.half_h = height / 2
        self.f = f
        self.width = width
        self.height = height
        slope = np.sqrt((pow(d, 2) + pow((width / 2), 2)))
        self.fov = 2 * np.arctan(self.half_h / slope)
        left_bottom_near = self.EYE + self.d * self.N - self.half_h * self.U - self.half_h * self.EYE_UP
        right_top_near = self.EYE + self.d * self.N + self.half_h * self.U + self.half_h * self.EYE_UP
        self.VIEW = np.array([left_bottom_near[0], right_top_near[0], left_bottom_near[1], right_top_near[1],
                              np.array([self.d]), np.array([self.f])])
        # self.VIEW = np.array([-5, 5, -5, 5, self.d, self.f])
        # self.LOOK_AT = self.EYE + self.PREF
        self.LOOK_AT = np.array([0, 0, 0])
        self.ProjectionMatrix = glm.perspective(self.fov,
                                                float(self.width) / float(self.height), self.d, self.f)

        self.calcView()
        self.calcMVP()

    def calcMVP(self, modelMaterix=glm.mat4(1.0)):
        self.calcView()
        self.MVP = self.ProjectionMatrix * self.ViewMatrix * modelMaterix

    def calcView(self):
        self.ViewMatrix = glm.lookAt(glm.vec3(self.EYE[0], self.EYE[1], self.EYE[2]),
                                     glm.vec3(self.LOOK_AT[0], self.LOOK_AT[1], self.LOOK_AT[2]),
                                     glm.vec3(self.vv[0], self.vv[1], self.vv[2])
                                     )


