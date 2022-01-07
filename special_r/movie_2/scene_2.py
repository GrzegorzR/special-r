import os
import glob
from math import pi, sin
from special_r.Scene import Scene
from special_r.movie_2.movie_2_objects import RhombusFractal
from special_r.movie_2.scene_1 import get_rhombus_tiling_positions
from special_r.utils.colorsets import chinskie
from special_r.utils.parametric_functions import create_smooth_transition_fun


def big_scale_down_test():
    colorset = chinskie
    # colorset = schiele_1
    # random.shuffle(colorset)
    x, y = 1960 / 2, 1080 / 2
    rhombus_list = []
    fun_q = lambda t: 400
    fun_p = lambda t: (sin((t * pi / 2))) * 90. + 300
    fun_p2 = fun_p
    pos = get_rhombus_tiling_positions(x, y)
    pos2 = get_rhombus_tiling_positions(x+1600, y)
    pos = pos + pos2
    border_squares = [0, 1, 2, 3, 5, 6, 9, 10, 12, 13, 14, 15]
    inside_squares = 4, 7, 8, 11
    f = create_smooth_transition_fun(1., 0.25, 0., 15)

    ft_scale = lambda t: (f(t), (x, y))

    for i, (x_r, y_r) in enumerate(pos):


        fun_p = lambda t: (sin((t * pi / 2)+x_r)) * 200. + 200
        fun_p2 = fun_p
        rhombus_list.append(RhombusFractal(x_r, y_r, fun_p2, fun_q, colorset))

    s = Scene(rhombus_list, bg_color=colorset[1], img_size=(1920, 1080))
    output_dir = 'out/movie_2/scene_2_test'

    for r in rhombus_list:
        r.scale_time_fun = ft_scale

    output_dir = None
    files = glob.glob('{}/*'.format(output_dir))

    if output_dir:
        for f in files:
            os.remove(f)
    s.animate(0.05, output_dir=output_dir, save_range=(0, 40 * 50))


if __name__ == '__main__':
    big_scale_down_test()