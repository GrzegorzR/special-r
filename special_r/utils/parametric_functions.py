from math import cos, sin, pi


def circle_clockwise(t):
    return sin(t), cos(t)


def circle_counterclockwise(t):
    return -sin(t), -cos(t+pi)


class ParametricCircle:
    def __init__(self, clockwise, phase=0):
        self.clockwise = clockwise
        self.phase = phase

    def __call__(self, *args, **kwargs):
        t = args[0]
        if self.clockwise:
            return sin(t + self.phase), cos(t + self.phase)
        else:
            return sin(t + self.phase), -cos(t + self.phase)
parametric_functions = {
    'clockwise': circle_clockwise,
    'counterclock': circle_counterclockwise
}