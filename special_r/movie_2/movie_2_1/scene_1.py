import glob
import os
from math import sin, pi

from special_r.Scene import Scene
from special_r.movie_2.movie_2_objects import RhombusFractal
from special_r.movie_2.scene_1 import get_rhombus_tiling_positions
from special_r.utils.colorsets import chinskie
from special_r.utils.parametric_functions import create_linear_transition_fun, create_smooth_transition_fun


def scene_1_1():
    colorset = chinskie
    # colorset = schiele_1
    # random.shuffle(colorset)
    # r = Rhombus(200, 200, 100, 200)
    x, y = 1960 / 2, 1080 / 2
    rhombus_list = []
    fun_q = lambda t: 400
    fun_p2 = lambda t: -sin((t * pi)) * 90. + 200
    # fun_p2 = lambda t: pow(2, cos(t / 2 + (pi / 2.))) * 90. + 308
    fun_p = lambda t: (sin((t * pi*2))) * 90. + 300





    pos = get_rhombus_tiling_positions(x, y)
    # fun_reverse_in = [1,2,7,8,9,10]
    border_squares = [0, 1, 2, 3, 5, 6, 9, 10, 12, 13, 14, 15]
    inside_squares = 4, 7, 8, 11
    for i, (x_r, y_r) in enumerate(pos):
        if i in inside_squares:
            fp, fq = fun_p2, fun_q
        else:
            fp, fq = fun_p, fun_q
        rhombus_list.append(RhombusFractal(x_r, y_r, fp, fq, colorset))

    scale_size_fun = create_linear_transition_fun(0., 1., 0, 30000)
    scale_t_fun = create_smooth_transition_fun(.2, 1., 0., 12., slope_param=3)
    scale_time_fun = lambda t: (scale_t_fun(t), None)
    for r in rhombus_list:
        r.scale_time_fun = scale_time_fun
        r.scale_size_fun = scale_size_fun

    # r4 = RhombusFractal(400+300/4, 400, (300/2.)*(3./5.), 300/2, colorset)
    # s = Scene([r1,r2,r3, r4], bg_color=colorset[0])
    s = Scene(rhombus_list, bg_color=colorset[1], img_size=(1920, 1080))
    output_dir = 'out/movie_2/scene_1_1'


    output_dir = None
    files = glob.glob('{}/*'.format(output_dir))

    if output_dir:
        for f in files:
            os.remove(f)
    s.animate(1 / 60, output_dir=output_dir, save_range=(0, 60 * 16))

if __name__ == '__main__':
    scene_1_1()