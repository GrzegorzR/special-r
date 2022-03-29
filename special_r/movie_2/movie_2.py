import glob
import math
import os
from math import sin, cos, pi
import random
import itertools

import numpy as np
import pygame
import pygame.gfxdraw

from special_r.Scene import Scene
from special_r.movie_2.movie_2_objects import RhombusFractal, HorRhombusFractal
from special_r.utils.colorsets import *
from special_r.utils.parametric_functions import create_transition_fun, create_linear_transition_fun, \
    create_smooth_transition_fun
from special_r.utils.callable_objects import CallableNumerical as CN


def old_note():
    # rhombus_list.append(RhombusFractal(x - 100, y + 100, fun_p, fun_q, colorset))
    # rhombus_list.append(RhombusFractal(x + 100, y - 100, fun_p2, fun_q, colorset))
    # rhombus_list.append(RhombusFractal(x - 300, y - 100, fun_p2, fun_q, colorset))
    # rhombus_list.append(RhombusFractal(x - 100, y - 300, fun_p, fun_q, colorset))

    # rhombus_list.append(RhombusFractal(x - 500, y - 300, fun_p, fun_q, colorset))
    # rhombus_list.append(RhombusFractal(x + 300, y - 300, fun_p, fun_q, colorset))
    # rhombus_list.append(RhombusFractal(x - 500, y + 100, fun_p, fun_q, colorset))
    # rhombus_list.append(RhombusFractal(x + 300, y + 100, fun_p, fun_q, colorset))

    # rhombus_list.append(RhombusFractal(x - 300, y - 500, fun_p2, fun_q, colorset))
    # rhombus_list.append(RhombusFractal(x + 100, y - 500, fun_p2, fun_q, colorset))
    # rhombus_list.append(RhombusFractal(x - 300, y + 300, fun_p2, fun_q, colorset))
    # rhombus_list.append(RhombusFractal(x + 100, y + 300, fun_p2, fun_q, colorset))
    pass


def scene_object_on_off():
    colorset = sorted(chinskie)
    # colorset = schiele_1
    # random.shuffle(colorset)
    # r = Rhombus(200, 200, 100, 200)
    x, y = 400, 400
    rhombus_list = []
    p_fun = lambda t: sin(t / 8) * 50 + 100
    q_fun = lambda t: sin(t / 4) * 100 + 300
    # p_fun = lambda t: 300
    q_fun = lambda t: 600
    p_fun = lambda t: 400

    trans_fun1 = create_transition_fun(0, 1, 0, 10, 20)
    trans_fun2 = create_transition_fun(0, 1, 8, 12, 4)
    scale_fun = lambda t: (trans_fun1(t), None)
    scale_fun2 = lambda t: (trans_fun2(t), None)

    # 400x = 600
    #
    # rhombus_list.append(RhombusFractal(400, 400, p_fun, q_fun, 0, colorset))
    rhombus_fractal = RhombusFractal(400, 400, p_fun, q_fun, colorset)
    rhombus_fractal2 = RhombusFractal(500, 400, CN(266 / 2), CN(400 / 2), colorset)
    rhombus_fractal3 = RhombusFractal(300, 400, CN(266 / 2), CN(400 / 2), colorset)

    rhombus_fractal4 = HorRhombusFractal(400, 500, CN(266 / 2), CN(400 / 2), colorset)
    rhombus_fractal5 = HorRhombusFractal(400, 300, CN(266 / 2), CN(400 / 2), colorset)

    rhombus_fractal.scale_time_fun = scale_fun
    rhombus_fractal2.scale_time_fun = scale_fun2
    rhombus_fractal3.scale_time_fun = scale_fun2
    rhombus_fractal4.scale_time_fun = scale_fun2
    rhombus_fractal5.scale_time_fun = scale_fun2

    rhombus_list += [rhombus_fractal, rhombus_fractal2, rhombus_fractal3, rhombus_fractal4, rhombus_fractal5]

    s = Scene(rhombus_list, bg_color=colorset[1])
    s.animate(0, output_dir=None, save_range=None)


def scene_size_with_scale():
    colorset = chinskie
    # colorset = to_zdjecie
    random.seed(12)
    random.shuffle(colorset)
    # colorset = chinskie
    # r = Rhombus(200, 200, 100, 200)
    x, y = 400, 400
    rhombus_list = []
    p_fun = lambda t: sin(t / 8) * 50 + 100
    q_fun = lambda t: sin(t / 4) * 100 + 300
    # p_fun = lambda t: 300
    q_fun = lambda t: 300
    p_fun = lambda t: 200
    f = create_smooth_transition_fun(1., 7.4, 0., 15)
    f2 = create_smooth_transition_fun(7.4, 1, 20, 30)

    # scale_time_fun = lambda t: ((cos(t/4) * 3. + 3.5), (400, 650))
    def scale_time_fun(t):
        if t < 15:
            return f(t), (450, 450)
        else:
            return f2(t), (450, 450)

    # scale_time_fun = lambda t: (f(t), (450, 450))
    # scale_time_fun = None

    scale_size_fun = create_linear_transition_fun(0., 1., 0, 20000)
    x_s = [150, 450, 750]
    y_s = [100, 300, 500, 700]
    rs_lvl_1 = []

    for x, y in itertools.product(x_s, y_s):
        rs_lvl_1.append(RhombusFractal(x, y, p_fun, q_fun, colorset))

    rs_lvl_2 = []
    for r in rs_lvl_1:
        rs_lvl_2 += r.get_objects_down()
    rs_lvl_3 = []
    for r in rs_lvl_2:
        rs_lvl_3 += r.get_objects_down()
    for r in rs_lvl_2:
        rs_lvl_3 += r.get_objects_down()

    rhombus_list = rs_lvl_1 + rs_lvl_2 + rs_lvl_3
    for r in rhombus_list:
        r.scale_size_fun = scale_size_fun
        r.scale_time_fun = scale_time_fun
    s = Scene(rhombus_list, bg_color=colorset[1])
    output_dir = 'out/movie_2/scene_scale_3'
    # output_dir = None
    s.animate(0.05, output_dir=output_dir, save_range=(0, 900))


def scene_qp_change():
    colorset = chinskie
    # colorset = to_zdjecie
    random.seed(12)
    random.shuffle(colorset)
    # colorset = chinskie
    # r = Rhombus(200, 200, 100, 200)
    x, y = 400, 400
    rhombus_list = []
    p_fun = lambda t: sin(t / 8) * 50 + 200
    # q_fun = lambda t: sin(t / 4) * 100 + 300
    # p_fun = lambda t: 300
    q_fun = lambda t: 300
    # p_fun = lambda t: 200
    f = create_smooth_transition_fun(1., 7.4, 0., 15)
    f2 = create_smooth_transition_fun(7.4, 1, 20, 30)
    scale_time_fun = None

    # scale_time_fun = lambda t: (f(t), (450, 450))
    # scale_time_fun = None

    scale_size_fun = create_linear_transition_fun(0., 1., 0, 20000)
    x_s = [150, 450, 750]
    y_s = [100, 300, 500, 700]
    rs_lvl_1 = []

    for x, y in itertools.product(x_s, y_s):
        rs_lvl_1.append(RhombusFractal(x, y, p_fun, q_fun, colorset))

    rs_lvl_2 = []
    for r in rs_lvl_1:
        rs_lvl_2 += r.get_objects_down()
    rs_lvl_3 = []
    for r in rs_lvl_2:
        rs_lvl_3 += r.get_objects_down()

    rhombus_list = rs_lvl_1 + rs_lvl_2 + rs_lvl_3
    for r in rhombus_list:
        r.scale_size_fun = scale_size_fun
        r.scale_time_fun = scale_time_fun
    s = Scene(rhombus_list, bg_color=colorset[1])
    output_dir = 'out/movie_2/scene_scale_3'
    output_dir = None
    s.animate(0.5, output_dir=output_dir, save_range=(0, 900))


if __name__ == '__main__':
    pass
    # scene_object_on_off()
    # scene_size_with_scale()
    # scene_qp_change()
    # scene_1()
