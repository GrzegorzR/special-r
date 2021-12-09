from math import cos, sin, pi
import numpy as np
from numpy import tanh


def circle_clockwise(t):
    return sin(t), cos(t)


def circle_counterclockwise(t):
    return -sin(t), -cos(t + pi)


class ParametricCircle:
    def __init__(self, clockwise, phase=0, r_speed=1.):
        self.clockwise = clockwise
        self.phase = phase
        self.r_speed = r_speed
    def __call__(self, *args, **kwargs):
        t = args[0]
        if self.clockwise:

            return sin(self.r_speed*t + self.phase)/10., cos(self.r_speed*t + self.phase)/10.
        else:
            return sin(-(self.r_speed*t + self.phase))/10., cos(-(self.r_speed*t + self.phase))/10.


class LissajousCurve:
    def __init__(self, kx=4, ky=1, a=1, b=1):
        self.kx = kx
        self.ky = ky
        self.a = a
        self.b = b

    def __call__(self, *args, **kwargs):
        t = args[0]
        return self.a * cos((t) * self.kx)/20, self.b * sin((t/2) * self.ky)/20

class ParametricSegment:
    def __init__(self, a=1):
        self.a = a

    def __call__(self, *args, **kwargs):
        t = args[0]
        return self.a*sin(t), 0


def saw_function(t):
    signal.sawtooth(2 * np.pi * 5 * t)

def create_transition_fun(v0, v1, t0, t1, slope_param=6.):
    # create smooth transition between values v0 and v1 in time t0 -> t1

    def out_fun(t):
        dt = t1 - t0
        dv = v1 - v0
        return ((tanh((t - t0 - (t1 - t0) / 2.) + slope_param / dt) + 1.) / 2.) * dv + v0

    return out_fun

def create_linear_transition_fun(v0, v1, t0, t1):
    def out_fun(t):
        if t > t1:
            return v1
        else:
            a = (v1-v0)/(t1 - t0)
            b = v0 - a*t0
        return a*t + b

    return out_fun


parametric_functions = {
    'clockwise': circle_clockwise,
    'counterclock': circle_counterclockwise
}


