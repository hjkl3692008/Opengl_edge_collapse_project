import numpy as np


class Animator(object):

    def __init__(self, animated_time=3 * 1000, step=100, final_fraction=0):
        self.animated_time = animated_time  # milli second(ms)
        self.step = step
        self.final_fraction = final_fraction
        self.each_step_time = int(self.animated_time / self.step)
        self.iteration = 0
        self.fraction = 0.0
        self.each_fraction = 1.0 / self.step

    def iterate(self):
        self.fraction = self.fraction + self.each_fraction
        if self.fraction > (1-self.final_fraction):
            self.fraction = (1-self.final_fraction)
            self.iteration = self.step
            return min(self.fraction, 1)
        else:
            self.iteration = self.iteration + 1
            return self.fraction
