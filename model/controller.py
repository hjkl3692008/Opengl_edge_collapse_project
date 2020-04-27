from OpenGL.GLUT import *

import numpy as np


class Controller:
    
    def __init__(self, window, update_f=None):
        self.window = window
        self.camera = window.camera
        self.mouse = window.mouse
        # distance, elevation, direction angle between eye and look point
        self.DIST, self.PHI, self.THETA = getposture(self.camera)
        self.update_function = update_f
    
    def mouseclick(self, button, state, x, y):
        self.mouse.MOUSE_X, self.mouse.MOUSE_Y = x, y
        if button == GLUT_LEFT_BUTTON:
            self.mouse.LEFT_IS_DOWNED = state == GLUT_DOWN
        elif button == 3:  # wheel up
            self.window.SCALE_K *= 1.05
            self.update_function()
        elif button == 4:  # wheel down
            self.window.SCALE_K *= 0.95
            self.update_function()

    def mousemotion(self, x, y):

        if self.mouse.LEFT_IS_DOWNED:
            dx = self.mouse.MOUSE_X - x
            dy = y - self.mouse.MOUSE_Y
            self.mouse.MOUSE_X, self.mouse.MOUSE_Y = x, y

            self.PHI += 2 * np.pi * dy / self.window.WIN_H
            self.PHI %= 2 * np.pi
            self.THETA += 2 * np.pi * dx / self.window.WIN_W
            self.THETA %= 2 * np.pi
            r = self.DIST * np.cos(self.PHI)

            self.camera.EYE[1] = self.DIST * np.sin(self.PHI)
            self.camera.EYE[0] = r * np.sin(self.THETA)
            self.camera.EYE[2] = r * np.cos(self.THETA)

            if 0.5 * np.pi < self.PHI < 1.5 * np.pi:
                self.camera.EYE_UP[1] = -1.0
            else:
                self.camera.EYE_UP[1] = 1.0

            self.update_function()

    def keydown(self, key, x, y):

        print('key input:' + str(key))

        if key in [b'x', b'X', b'y', b'Y', b'z', b'Z']:
            if key == b'x':  # decrease x
                self.camera.LOOK_AT[0] -= 0.01 * self.mouse.MOVE_SPEED
            elif key == b'X':  # increase x
                self.camera.LOOK_AT[0] += 0.01 * self.mouse.MOVE_SPEED
            elif key == b'y':  # decrease y
                self.camera.LOOK_AT[1] -= 0.01 * self.mouse.MOVE_SPEED
            elif key == b'Y':  # increase y
                self.camera.LOOK_AT[1] += 0.01 * self.mouse.MOVE_SPEED
            elif key == b'z':  # decrease z
                self.camera.LOOK_AT[2] -= 0.01 * self.mouse.MOVE_SPEED
            elif key == b'Z':  # increase z
                self.camera.LOOK_AT[2] += 0.01 * self.mouse.MOVE_SPEED
        elif key in [b'w', b'a', b's', b'd']:
            if key == b'w':  # move up
                self.camera.LOOK_AT[0] += 0.01 * self.mouse.MOVE_SPEED
                self.camera.EYE[0] += 0.01 * self.mouse.MOVE_SPEED
            elif key == b'a':  # move left
                self.camera.LOOK_AT[1] -= 0.01 * self.mouse.MOVE_SPEED
                self.camera.EYE[1] -= 0.01 * self.mouse.MOVE_SPEED
            elif key == b's':  # move down
                self.camera.LOOK_AT[0] -= 0.01 * self.mouse.MOVE_SPEED
                self.camera.EYE[0] -= 0.01 * self.mouse.MOVE_SPEED
            elif key == b'd':  # move right
                self.camera.LOOK_AT[1] += 0.01 * self.mouse.MOVE_SPEED
                self.camera.EYE[1] += 0.01 * self.mouse.MOVE_SPEED
        elif key == b'\r':  # enter, view forward
            self.camera.EYE = self.camera.LOOK_AT + (self.camera.EYE - self.camera.LOOK_AT) * 0.9
        elif key == b'\x08':  # backspace, view back
            self.camera.EYE = self.camera.LOOK_AT + (self.camera.EYE - self.camera.LOOK_AT) * 1.1
        elif key == b' ':  # space, change project mode
            self.window.IS_PERSPECTIVE = not self.window.IS_PERSPECTIVE

        self.DIST, self.PHI, self.THETA = getposture(self.camera)
        self.update_function()
            

# calculate posture
def getposture(camera):
    dist = np.sqrt(np.power((camera.EYE - camera.LOOK_AT), 2).sum())
    if dist > 0:
        phi = np.arcsin((camera.EYE[1] - camera.LOOK_AT[1]) / dist)
        theta = np.arcsin((camera.EYE[0] - camera.LOOK_AT[0]) / (dist * np.cos(phi)))
    else:
        phi = 0.0
        theta = 0.0

    return dist, phi, theta
