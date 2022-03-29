import os
import glob
import random

# random.seed(21377)
from special_r.movie_2.scene_2 import rotate

random.seed(1)
from math import pi, sin, sqrt
from special_r.Scene import Scene
from special_r.movie_2.movie_2_objects import RhombusFractal
from special_r.movie_2.scene_1 import get_rhombus_tiling_positions
from special_r.utils.colorsets import chinskie, blue_crystal_vienna
from special_r.utils.parametric_functions import create_smooth_transition_fun, create_linear_transition_fun


class Scene3(Scene):
    def __init__(self, objects, f_s, f_t, f_r):
        super().__init__(objects)


def scene_3_0():

    x, y = 1960 / 2, 1080 / 2
    rhombus_list = []
    fun_q = lambda t: 400
    fun_p2 = lambda t: -sin((t * pi * 2)) * 90. + 200
    fun_p = lambda t: (sin((t * pi * 2))) * 90. + 300

    pos = []
    pos += get_rhombus_tiling_positions(x, y)

    pos += get_rhombus_tiling_positions(x + 1600, y)
    pos += get_rhombus_tiling_positions(x - 1600, y)
    pos += get_rhombus_tiling_positions(x, y + 1600)
    pos += get_rhombus_tiling_positions(x, y - 1600)

    pos += get_rhombus_tiling_positions(x + 3200, y)
    pos += get_rhombus_tiling_positions(x + 1600, y - 1600)

    pos += get_rhombus_tiling_positions(x + 2400, y - 800)
    pos += get_rhombus_tiling_positions(x + 800, y - 2400)
    pos += get_rhombus_tiling_positions(x, y - 3200)
    pos += get_rhombus_tiling_positions(x - 800, y - 2400)

    pos += get_rhombus_tiling_positions(x - 2400, y + 800)
    pos += get_rhombus_tiling_positions(x - 800, y + 2400)
    pos += get_rhombus_tiling_positions(x, y + 3200)
    pos += get_rhombus_tiling_positions(x + 800, y + 2400)
    pos += get_rhombus_tiling_positions(x - 3200, y)
    pos += get_rhombus_tiling_positions(x - 1600, y + 1600)

    pos += get_rhombus_tiling_positions(x - 1600, y - 1600)
    pos += get_rhombus_tiling_positions(x - 2400, y - 800)
    pos += get_rhombus_tiling_positions(x + 1600, y + 1600)
    pos += get_rhombus_tiling_positions(x + 2400, y + 800)

    border_squares = [0, 1, 2, 3, 5, 6, 9, 10, 12, 13, 14, 15]
    inside_squares = 4, 7, 8, 11
    f_s = create_smooth_transition_fun(0.15, 1., 0., 2.5)
    f_t_x = create_smooth_transition_fun(0, -2000, 0, 2.5)
    f_t_y = create_smooth_transition_fun(0, -1000, 0, 2.5)
    translations_fun = lambda t: (f_t_x(t), f_t_y(t))

    rec_center_pos = x, y
    ft_scale = lambda t: (f_s(t), (x, y))

    for i, (x_r, y_r) in enumerate(pos):
        dist_from_center = sqrt((x_r - x) ** 2 + (y_r - y) ** 2)
        if i in inside_squares:
            fp, fq = fun_p2, fun_q
        else:
            fp, fq = fun_p, fun_q

        if i < 16 * 5:
            colorset = chinskie
        else:
            colorset = rotate(chinskie, int(dist_from_center+3)%5)
        rhombus_list.append(RhombusFractal(x_r, y_r, fp, fq, colorset, debug=False))

    s = Scene(rhombus_list, bg_color=chinskie[1], img_size=(1920, 1080))
    output_dir = 'out/movie_2/scene_3_0'
    # output_dir = None

    for r in rhombus_list:
        r.scale_time_fun = ft_scale
        r.translations_fun = translations_fun

    files = glob.glob('{}/*'.format(output_dir))

    if output_dir:
        for f in files:
            os.remove(f)
    dt = 1 / 60
    # dt = 0.5
    s.animate(dt, output_dir=output_dir, save_range=(0, 60 * 8))


def scene_3_1():
    colorset = chinskie

    # colorset = schiele_1
    # random.shuffle(colorset)
    x, y = 1960 / 2, 1080 / 2
    rhombus_list = []
    fun_q = lambda t: 400
    f_down = create_smooth_transition_fun(1, 0, 0, 5, slope_param=3)
    fun_p2 = lambda t: -sin((t * pi * 2)) * f_down(t) * 90. + 200
    fun_p = lambda t: (sin((t * pi * 2))) * f_down(t) * 90. + 300

    pos = []
    pos += get_rhombus_tiling_positions(x + 1600, y)
    pos += get_rhombus_tiling_positions(x - 1600, y - 1600)
    pos += get_rhombus_tiling_positions(x + 1600, y + 1600)
    pos += get_rhombus_tiling_positions(x + 2400, y + 800)

    border_squares = [0, 1, 2, 3, 5, 6, 9, 10, 12, 13, 14, 15]
    inside_squares = 4, 7, 8, 11
    f_s = create_smooth_transition_fun(1, 1, 0., 5)
    f_t_x = create_smooth_transition_fun(-2000, -2000, 0, 5)
    f_t_y = create_smooth_transition_fun(-1000, -1000, 0, 5)
    translations_fun = lambda t: (f_t_x(t), f_t_y(t))

    rec_center_pos = x, y
    ft_scale = lambda t: (f_s(t), (x, y))

    for i, (x_r, y_r) in enumerate(pos):
        if i in inside_squares:
            fp, fq = fun_p2, fun_q
        else:
            fp, fq = fun_p, fun_q

        if i < 16 * 5:
            colorset = chinskie
        else:
            # colorset = blue_crystal_vienna
            colorset = random.sample(chinskie, len(chinskie))
        rhombus_list.append(RhombusFractal(x_r, y_r, fp, fq, colorset, debug=False))
    s = Scene(rhombus_list, bg_color=chinskie[1], img_size=(1920, 1080))

    for r in rhombus_list:
        r.scale_time_fun = ft_scale
        r.translations_fun = translations_fun

    output_dir = 'out/movie_2/scene_3_1'
    # output_dir = None

    files = glob.glob('{}/*'.format(output_dir))

    if output_dir:
        for f in files:
            os.remove(f)
    dt = 1 / 60
    # dt = 0.5
    s.animate(dt, output_dir=output_dir, save_range=(0, 60 * 8))


def scene_3_1_5():
    x, y = 1960 / 2, 1080 / 2
    rhombus_list = []
    fun_q = lambda t: 400
    fun_p2 = lambda t: 200
    fun_p = lambda t: 300

    pos = []
    pos += get_rhombus_tiling_positions(x + 1600, y)
    pos += get_rhombus_tiling_positions(x - 1600, y - 1600)
    pos += get_rhombus_tiling_positions(x + 1600, y + 1600)
    pos += get_rhombus_tiling_positions(x + 2400, y + 800)

    f_t_x = create_smooth_transition_fun(-2000, -2000, 0, 2.5)
    f_t_y = create_smooth_transition_fun(-1000, -1000, 0, 2.5)
    translations_fun = lambda t: (f_t_x(t), f_t_y(t))

    for i, (x_r, y_r) in enumerate(pos):

        fp, fq = fun_p, fun_q

        if i < 16 * 5:
            colorset = chinskie
            # random.seed(2197)
            # colorset = random.sample(chinskie, len(chinskie))
        else:
            # colorset = blue_crystal_vienna
            colorset = random.sample(chinskie, len(chinskie))
        rhombus_list.append(RhombusFractal(x_r, y_r, fp, fq, colorset, debug=False))

    down_index_list = [58, 52, 53]
    lv2 = []
    for ind in down_index_list:
        lv2 += rhombus_list[ind].get_objects_down()
    #lv2 = [rhombus_list[ind].get_objects_down() for ind in down_index_list]

    # lv2 = rhombus_list[58].get_objects_down() + rhombus_list[52].get_objects_down()
    # lv2= []
    # lv3 = []
    # for r in lv2:
    #    lv3 += r.get_objects_down()

    lvls_down = lv2
    scale_size_fun = create_linear_transition_fun(0., 1., 0, 30000)
    scale_t_fun = create_smooth_transition_fun(1., 1., 0., 4., slope_param=3)
    scale_time_fun = lambda t: (scale_t_fun(t), None)
    for r in lvls_down:
        r.scale_time_fun = scale_time_fun
        r.scale_size_fun = scale_size_fun

    rhombus_list += lvls_down
    for r in rhombus_list:
        # r.scale_time_fun = scale_time_fun
        r.translations_fun = translations_fun

    s = Scene(rhombus_list, bg_color=chinskie[1], img_size=(1920, 1080))
    output_dir = 'out/movie_2/scene_3_1_5'
    output_dir = None

    files = glob.glob('{}/*'.format(output_dir))

    if output_dir:
        for f in files:
            os.remove(f)
    dt = 1 / 60
    # dt = 0.1
    s.animate(dt, output_dir=output_dir, save_range=(0, 60 * 8))


def scene_3_2():
    colorset = chinskie
    # colorset = schiele_1
    # random.shuffle(colorset)
    x, y = 1960 / 2, 1080 / 2
    rhombus_list = []
    fun_q = lambda t: 400
    f_down = create_smooth_transition_fun(1, 0, 0, 5, slope_param=3)
    fun_p2 = lambda t: 200
    fun_p = lambda t: 300

    pos = []
    pos += get_rhombus_tiling_positions(x + 1600, y)
    pos += get_rhombus_tiling_positions(x - 1600, y - 1600)
    pos += get_rhombus_tiling_positions(x + 1600, y + 1600)
    pos += get_rhombus_tiling_positions(x + 2400, y + 800)

    border_squares = [0, 1, 2, 3, 5, 6, 9, 10, 12, 13, 14, 15]
    inside_squares = 4, 7, 8, 11
    f1 = create_smooth_transition_fun(1, 1.5, 0., 4., slope_param=16)
    f2 = create_smooth_transition_fun(1.5, 2.5, 4, 8, slope_param=16)
    f3 = create_smooth_transition_fun(2.5, 5, 8, 12)

    def f_s(t):
        # print(t)
        if t < 4:
            return f1(t)

        elif 4 <= t < 8:
            return f2(t)
        else:
            return f3(t)

    f_t_x = create_smooth_transition_fun(-2000, -2000, 0, 2.5)
    f_t_y = create_smooth_transition_fun(-1000, -1000, 0, 2.5)
    translations_fun = lambda t: (f_t_x(t), f_t_y(t))

    rec_center_pos = x, y
    ft_scale = lambda t: (f_s(t), (x, y))

    for i, (x_r, y_r) in enumerate(pos):
        if i in inside_squares:
            fp, fq = fun_p2, fun_q
        else:
            fp, fq = fun_p, fun_q

        if i < 16 * 5:
            colorset = chinskie
            # random.seed(2197)

            # colorset = random.sample(chinskie, len(chinskie))
        else:
            # colorset = blue_crystal_vienna
            colorset = random.sample(chinskie, len(chinskie))
        rhombus_list.append(RhombusFractal(x_r, y_r, fp, fq, colorset, debug=False))

    # del rhombus_list[52]
    rhombus_list[58].colorset = chinskie
    lv2 = rhombus_list[58].get_objects_down() + rhombus_list[52].get_objects_down()

    lv3 = []
    for r in lv2:
        lv3 += r.get_objects_down()

    lvls_down = lv2 + lv3
    scale_size_fun = create_linear_transition_fun(0., 1., 0, 30000)
    for r in lvls_down:
        r.scale_size_fun = scale_size_fun

    rhombus_list += lvls_down

    for r in rhombus_list:
        r.scale_time_fun = ft_scale
        r.translations_fun = translations_fun

    s = Scene(rhombus_list, bg_color=chinskie[1], img_size=(1920, 1080))
    output_dir = 'out/movie_2/scene_3_2'
    # output_dir = None

    files = glob.glob('{}/*'.format(output_dir))

    if output_dir:
        for f in files:
            os.remove(f)
    dt = 1 / 60
    # dt = 0.1
    s.animate(dt, output_dir=output_dir, save_range=(0, 60 * 16))


if __name__ == '__main__':
    scene_3_0()
    # scene_3_1()
    #scene_3_1_5()
    # scene_3_2()
