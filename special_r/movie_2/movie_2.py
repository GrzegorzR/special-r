import math
from math import sin, cos, pi
import random

import numpy as np
import pygame
import pygame.gfxdraw

from special_r.Scene import Scene
from special_r.movie_2.movie_2_objects import RhombusFractal, HorRhombusFractal
from special_r.utils.colorsets import *
from special_r.utils.parametric_functions import create_transition_fun, create_linear_transition_fun
from special_r.utils.callable_objects import CallableNumerical as CN


def scene_1():
    colorset = chinskie
    # colorset = schiele_1
    # random.shuffle(colorset)
    # r = Rhombus(200, 200, 100, 200)
    x, y = 500, 500
    rhombus_list = []
    fun_q = lambda t: 400
    fun_p2 = lambda t: (cos(t + (pi / 2.))) * 90. + 308
    fun_p = lambda t: (sin(t)) * 90. + 308
    rhombus_list.append(RhombusFractal(x - 100, y + 100, fun_p, fun_q, colorset))
    rhombus_list.append(RhombusFractal(x + 100, y - 100, fun_p2, fun_q, colorset))
    rhombus_list.append(RhombusFractal(x - 300, y - 100, fun_p2, fun_q, colorset))
    rhombus_list.append(RhombusFractal(x - 100, y - 300, fun_p, fun_q, colorset))

    rhombus_list.append(RhombusFractal(x - 500, y - 300, fun_p, fun_q, colorset))
    rhombus_list.append(RhombusFractal(x + 300, y - 300, fun_p, fun_q, colorset))
    rhombus_list.append(RhombusFractal(x - 500, y + 100, fun_p, fun_q, colorset))
    rhombus_list.append(RhombusFractal(x + 300, y + 100, fun_p, fun_q, colorset))

    rhombus_list.append(RhombusFractal(x - 300, y - 500, fun_p2, fun_q, colorset))
    rhombus_list.append(RhombusFractal(x + 100, y - 500, fun_p2, fun_q, colorset))
    rhombus_list.append(RhombusFractal(x - 300, y + 300, fun_p2, fun_q, colorset))
    rhombus_list.append(RhombusFractal(x + 100, y + 300, fun_p2, fun_q, colorset))
    # r4 = RhombusFractal(400+300/4, 400, (300/2.)*(3./5.), 300/2, colorset)
    # s = Scene([r1,r2,r3, r4], bg_color=colorset[0])
    s = Scene(rhombus_list, bg_color=colorset[1])
    s.animate(0, output_dir=None, save_range=(0, 4000))


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
    colorset = list(reversed(sorted(chinskie)))
    # colorset = to_zdjecie
    #random.shuffle(colorset)
    #colorset = chinskie
    # r = Rhombus(200, 200, 100, 200)
    x, y = 400, 400
    rhombus_list = []
    p_fun = lambda t: sin(t / 8) * 50 + 100
    q_fun = lambda t: sin(t / 4) * 100 + 300
    # p_fun = lambda t: 300
    q_fun = lambda t: 600
    p_fun = lambda t: 400
    scale_time_fun = lambda t: ((sin(t/2) * 2 + 2), (500, 400))
    scale_size_fun = create_linear_transition_fun(0., 1., 0, 40000)

    rhombus_fractal = RhombusFractal(400, 400, p_fun, q_fun, colorset)
    r2 = rhombus_fractal.get_objects_down()
    r3 = []
    for r in r2:
        r3 += r.get_objects_down()

    rhombus_list = [rhombus_fractal] + r2 + r3
    for r in rhombus_list:
        r.scale_size_fun = scale_size_fun
        r.scale_time_fun = scale_time_fun
    s = Scene(rhombus_list, bg_color=colorset[1])
    output_dir ='out/movie_2/scene_scale_1'
    output_dir = None
    s.animate(0.05, output_dir=output_dir, save_range=(0,1000))


if __name__ == '__main__':
    # scene_object_on_off()
    scene_size_with_scale()
    # scene_1()
