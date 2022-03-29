from math import cos, sin, pi
import numpy as np
from numpy import tanh
import matplotlib.pyplot as plt


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

            return sin(self.r_speed * t + self.phase) / 10., cos(self.r_speed * t + self.phase) / 10.
        else:
            return sin(-(self.r_speed * t + self.phase)) / 10., cos(-(self.r_speed * t + self.phase)) / 10.


class LissajousCurve:
    def __init__(self, kx=4, ky=1, a=1, b=1):
        self.kx = kx
        self.ky = ky
        self.a = a
        self.b = b

    def __call__(self, *args, **kwargs):
        t = args[0]
        return self.a * cos((t) * self.kx) / 20, self.b * sin((t / 2) * self.ky) / 20


class ParametricSegment:
    def __init__(self, a=1):
        self.a = a

    def __call__(self, *args, **kwargs):
        t = args[0]
        return self.a * sin(t), 0


def saw_function(t):
    signal.sawtooth(2 * np.pi * 5 * t)


def create_transition_fun(v0, v1, t0, t1, slope_param=6.):
    # create smooth transition between values v0 and v1 in time t0 -> t1

    def out_fun(t):
        dt = t1 - t0
        dv = v1 - v0
        return ((tanh((t - t0 - (t1 - t0) / 2.) + slope_param / dt) + 1.) / 2.) * dv + v0

    return out_fun


def create_smooth_transition_fun(v0, v1, t0, t1, slope_param=6.):
    # f(x) = (tanh((x - t0_1 - (t1_1 - t0_1) / 2) c / (t1_1 - t0_1)) + 1) / 2 (v1_1 - v0_1) + v0_1
    def out(x):
        if x < t0:
            return v0
        if x > t1:
            return v1
        v = (tanh((x - t0 - (t1 - t0) / 2.) * slope_param / (t1 - t0)) + 1) / 2 * (v1 - v0) + v0
        return v

    return out


def create_linear_transition_fun(v0, v1, t0, t1):
    def out_fun(t):
        if t > t1:
            return v1
        if t < t0:
            return v0
        a = (v1 - v0) / (t1 - t0)
        b = v0 - a * t0
        return a * t + b

    return out_fun


parametric_functions = {
    'clockwise': circle_clockwise,
    'counterclock': circle_counterclockwise
}


def concatenate_functions(funs, time_ranges):
    def out_fun(t):
        if t < time_ranges[0][0]:
            return funs[0](t)
        if t > time_ranges[-1][1]:
            return funs[-1](t)
        for i, r in enumerate(time_ranges):
            if r[0] <= t < r[1]:
                return funs[i](t)

    return out_fun


def compare_transition_functions():
    v0, v1 = 2, 11
    t0, t1 = 0, 50
    f1 = create_transition_fun(v0, v1, t0, t1)
    f2 = create_smooth_transition_fun(v0, v1, t0, t1)
    f3 = create_linear_transition_fun(v0, v1, t0, t1)

    t = np.arange(t0 - 10, t1 + 10, 0.1)
    v1 = np.array(list(map(f1, t)))
    v2 = np.array(list(map(f2, t)))
    v3 = np.array(list(map(f3, t)))

    plt.gca().set_aspect('equal', adjustable='box')

    plt.plot(t, v1)
    plt.plot(t, v2)
    plt.plot(t, v3)
    plt.axvline(x=t0, c='red')
    plt.axvline(x=t1, c='red')
    plt.show()


if __name__ == '__main__':
    v0, v1 = 2, 11

    f1 = create_linear_transition_fun(v0, v1, 0, 10)
    f2 = create_smooth_transition_fun(v1, v0-5, 15, 20)

    f_con = concatenate_functions([f1, f2], [(0, 10), (10, 25)])
    t = np.arange(-10, 40, 0.1)
    v1 = np.array(list(map(f_con, t)))

    plt.gca().set_aspect('equal', adjustable='box')

    plt.plot(t, v1)
    plt.show()
