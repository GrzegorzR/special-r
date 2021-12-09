import itertools
from math import pi, sin, cos

from special_r.movie_1.utils import PyramidsScene
from special_r.pyramid.Pyramid import PyramidMoving
from special_r.utils.colorsets import *
from special_r.utils.parametric_functions import ParametricCircle, LissajousCurve

c = list(reversed(schiele_1))

def get_square_grid_pos(borders, nums, sizes, img_size):
    border_x, border_y = borders
    num_x, num_y = nums
    size_x, size_y = sizes
    w, h = img_size

    out = [[None for _ in range(num_x)] for _ in range(num_y)]
    for x, y in itertools.product(range(num_x), range(num_y)):

        pym_x = border_x + x*((w - 2*border_x )/(num_x-1))
        pym_y = border_y + y * ((h - 2 * border_y) / (num_y - 1))

        out[x][y] = (pym_x, pym_y)

    return out

def get_pyms_scene_6():
    center_x, center_y = 1920 / 2, 1080/2



    c = list(reversed(schiele_1))
    w, h = 200, 200
    pyramides = []
    dt = 0.08
    steps = 16 * pi / dt
    print(steps, dt)
    for x in range(0, 4):
        for y in range(0, 4):
            clockwise = False
            phase = pi * x / 4 + pi * y / 8
            if x > 1 and y < 2:
                clockwise = False
            if x > 1 and y > 1:
                clockwise = False
            p = PyramidMoving(700 + x * 200, 200 + y * 200, w, h, ParametricCircle(clockwise, phase),
                              colors=c, scale=0.75, height=10, borders_colors=c)
            pyramides.append(p)

    return pyramides

def get_scene_6_obj():
    bg_color = c[0]
    dt = 0.05
    return PyramidsScene(get_pyms_scene_6, 250, dt, bg_color, img_size=(1920, 1080))


if __name__ == '__main__':
    s = get_scene_6_obj()
    s.display()