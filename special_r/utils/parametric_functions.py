from math import cos, sin, pi
from numpy import tanh


def circle_clockwise(t):
    return sin(t), cos(t)


def circle_counterclockwise(t):
    return -sin(t), -cos(t + pi)


class ParametricCircle:
    def __init__(self, clockwise, phase=0, r_speed=1.):
        self.clockwise = clockwise
        self.phase = -pi/8.
        self.r_speed = r_speed
    def __call__(self, *args, **kwargs):
        t = args[0]
        if self.clockwise:

            return sin(self.r_speed*t + self.phase), cos(self.r_speed*t + self.phase)
        else:
            return -sin(self.r_speed*t + self.phase), -cos(self.r_speed*t + self.phase)


class LissajousCurve:
    def __init__(self, kx=4, ky=3, a=4, b=4):
        self.kx = kx
        self.ky = ky
        self.a = a
        self.b = b

    def __call__(self, *args, **kwargs):
        t = args[0]
        return self.a * cos((t/2) * self.kx), self.b * sin((t/2) * self.ky)


class ParametricSegment:
    def __init__(self, a=1):
        self.a = a

    def __call__(self, *args, **kwargs):
        t = args[0]
        return self.a*sin(t), 0


def create_transition_fun(v0, v1, t0, t1, slope_param=6.):
    # create smooth transition between values v0 and v1 in time t0 -> t1

    def out_fun(t):
        dt = t1 - t0
        dv = v1 - v0
        return ((tanh((t - t0 - (t1 - t0) / 2.) + slope_param / dt) + 1.) / 2.) * dv + v0

    return out_fun

parametric_functions = {
    'clockwise': circle_clockwise,
    'counterclock': circle_counterclockwise
}
