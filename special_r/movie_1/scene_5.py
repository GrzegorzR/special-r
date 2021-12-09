import itertools
from math import pi, sin, cos

from special_r.examples.state_pym import StatePym
from special_r.movie_1.scene_1 import get_colorset as get_scene_1_colorsets, get_xyt as get_scene_1_xyt
from special_r.movie_1.scene_1 import get_positions as get_scene_1_positions, get_sizes as get_scene_1_sizes

from special_r.movie_1.scene_1 import get_borders_colors as get_scene_1_colorsets_border_colors
from special_r.movie_1.utils import PyramidsScene
from special_r.pyramid.Pyramid import PyramidMoving
from special_r.utils.colorsets import *

from special_r.utils.parametric_functions import ParametricCircle, LissajousCurve

c = list(reversed(white_to_green(13)))


def get_square_grid_pos(borders, nums, sizes, img_size):
    border_x, border_y = borders
    num_x, num_y = nums
    size_x, size_y = sizes
    w, h = img_size

    out = [[None for _ in range(num_x)] for _ in range(num_y)]
    for x, y in itertools.product(range(num_x), range(num_y)):
        pym_x = border_x + x * ((w - 2 * border_x) / (num_x - 1))
        pym_y = border_y + y * ((h - 2 * border_y) / (num_y - 1))

        out[x][y] = (pym_x, pym_y)
    return out


def get_row(center_y, parameter, parameter2):
    center_x = 1920 / 2
    size_fun_1 = lambda t: (
        100 * (sin(t + (parameter * pi / 16)) + 2) + 100, (100 * (parameter2 * sin(t * pi / 16) + 2)))
    size_fun_2 = lambda t: (
        100 * (-sin(t + (parameter * pi / 16)) + 2) + 100, (100 * (parameter2 * sin(t * pi / 16) + 2)))

    p = PyramidMoving(center_x, center_y, 200, 200, lambda t: (0, 0), colors=c, borders_colors=c, scale=0.9, height=13)
    p.size_fun = size_fun_1

    p2 = PyramidMoving(center_x + 300, center_y, 200, 200, lambda t: (0, 0), colors=c, borders_colors=c, scale=0.9,
                       height=13)
    p2.size_fun = size_fun_2

    p3 = PyramidMoving(center_x - 300, center_y, 200, 200, lambda t: (0, 0), colors=c, borders_colors=c, scale=0.9,
                       height=13)
    p3.size_fun = size_fun_2

    p4 = PyramidMoving(center_x - 600, center_y, 200, 200, lambda t: (0, 0), colors=c, borders_colors=c, scale=0.9,
                       height=13)
    p4.size_fun = size_fun_1

    p5 = PyramidMoving(center_x - 900, center_y, 200, 200, lambda t: (0, 0), colors=c, borders_colors=c, scale=0.9,
                       height=13)
    p5.size_fun = size_fun_2

    p6 = PyramidMoving(center_x + 600, center_y, 200, 200, lambda t: (0, 0), colors=c, borders_colors=c, scale=0.9,
                       height=13)
    p6.size_fun = size_fun_1

    p7 = PyramidMoving(center_x + 900, center_y, 200, 200, lambda t: (0, 0), colors=c, borders_colors=c, scale=0.9,
                       height=13)
    p7.size_fun = size_fun_2

    pyms = [p, p2, p3, p4, p5, p6, p7]

    return pyms


def get_pyms_scene_5():
    center_y = 1080 / 2
    pyms = get_row(center_y, 0, 1)
    pyms += get_row(center_y + 200, 1, -1)
    pyms += get_row(center_y + 400, 2, 1)
    pyms += get_row(center_y + 600, 3, -1)

    pyms += get_row(center_y - 200, -1, -1)
    pyms += get_row(center_y - 400, -2, 1)
    pyms += get_row(center_y - 600, -3, -1)

    for p in pyms:
        p.update(0.01)

    return pyms


def get_pyms_scene_5_2():
    transitions_time = 10.
    poses = get_scene_1_positions()
    poses = [p[1:3] for p in poses]

    xyt_arr = get_scene_1_xyt()
    xyt_arr = [p[1:3] for p in xyt_arr]

    sizes = get_scene_1_sizes()
    sizes = [p[1:3] for p in sizes]

    pyms = []
    colorsets = get_scene_1_colorsets(13)
    border_colors = get_scene_1_colorsets_border_colors(13)

    for i in range(len(poses)):
        states = {
            'pos': poses[i],
            'xyt': xyt_arr[i],
            'scale': [0.92, 0.92],
            'size': sizes[i]
        }

        p = StatePym(states, transitions_time, 13, colorsets[i], borders_colors=border_colors[i])
        pyms.append(p)
    return pyms


def get_scene_5_obj():
    bg_color = c[1]
    dt = 0.05
    scene_1_colorsets = itertools.cycle(get_scene_1_colorsets(13))
    scene_1_borders_colors = itertools.cycle(get_scene_1_colorsets_border_colors(13))

    class Scene5(PyramidsScene):
        def update_rule(self):
            if self.c == 500:
                for p in self.objects:
                    p.change_colorset(next(scene_1_colorsets))
                    p.change_borders_colorstes(next(scene_1_borders_colors))

    return Scene5(get_pyms_scene_5, 1000, dt, bg_color, img_size=(1920, 1080))


def get_scene_5_2_obj():
    bg_color = '#82808A'
    dt = 0.05
    return PyramidsScene(get_pyms_scene_5_2, 200, dt, bg_color, img_size=(1920, 1080))


if __name__ == '__main__':
    s = get_scene_5_2_obj()
    s.display()
