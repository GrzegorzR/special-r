import os
import glob
import random
random.seed(21377)
from math import pi, sin, sqrt
from special_r.Scene import Scene
from special_r.movie_2.movie_2_objects import RhombusFractal
from special_r.movie_2.scene_1 import get_rhombus_tiling_positions
from special_r.utils.colorsets import chinskie, blue_crystal_vienna
from special_r.utils.parametric_functions import create_smooth_transition_fun


def rotate(l, n):
    return l[n:] + l[:n]


def scene_2():
    colorset = chinskie
    # colorset = schiele_1
    # random.shuffle(colorset)
    x, y = 1960 / 2, 1080 / 2
    rhombus_list = []
    fun_q = lambda t: 400
    fun_p2 = lambda t: -sin((t * pi)) * 90. + 200
    fun_p = lambda t: (sin((t * pi ))) * 90. + 300

    pos =[]
    pos += get_rhombus_tiling_positions(x, y)

    pos += get_rhombus_tiling_positions(x+1600, y)
    pos += get_rhombus_tiling_positions(x-1600, y)
    pos += get_rhombus_tiling_positions(x, y+1600)
    pos += get_rhombus_tiling_positions(x, y-1600)

    pos += get_rhombus_tiling_positions(x+3200, y)
    pos += get_rhombus_tiling_positions(x + 1600, y-1600)

    pos += get_rhombus_tiling_positions(x + 2400, y-800)
    pos += get_rhombus_tiling_positions(x + 800, y-2400 )
    pos += get_rhombus_tiling_positions(x , y - 3200)
    pos += get_rhombus_tiling_positions(x -800, y - 2400)

    pos += get_rhombus_tiling_positions(x - 2400, y+800)
    pos += get_rhombus_tiling_positions(x - 800, y+2400 )
    pos += get_rhombus_tiling_positions(x , y + 3200)
    pos += get_rhombus_tiling_positions(x +800, y + 2400)
    pos += get_rhombus_tiling_positions(x-3200, y)
    pos += get_rhombus_tiling_positions(x - 1600, y+1600)

    pos += get_rhombus_tiling_positions(x - 1600, y - 1600)
    pos += get_rhombus_tiling_positions(x - 2400, y - 800)
    pos += get_rhombus_tiling_positions(x + 1600, y + 1600)
    pos += get_rhombus_tiling_positions(x + 2400, y + 800)



    border_squares = [0, 1, 2, 3, 5, 6, 9, 10, 12, 13, 14, 15]
    inside_squares = 4, 7, 8, 11
    f = create_smooth_transition_fun(1., 0.15, 0., 4.)
    ft_scale = lambda t: (f(t), (x, y))

    for i, (x_r, y_r) in enumerate(pos):

        if i in inside_squares:
            fp, fq = fun_p2, fun_q
        else:
            fp, fq = fun_p, fun_q

        if i < 16*5:
            colorset = chinskie
        else:
            #colorset = blue_crystal_vienna
            colorset = random.sample(chinskie, len(chinskie))
        rhombus_list.append(RhombusFractal(x_r, y_r, fp, fq, colorset))

    s = Scene(rhombus_list, bg_color=chinskie[1], img_size=(1920, 1080))
    output_dir = 'out/movie_2/scene_2'
    #output_dir = None

    for r in rhombus_list:
        r.scale_time_fun = ft_scale


    files = glob.glob('{}/*'.format(output_dir))

    if output_dir:
        for f in files:
            os.remove(f)
    s.animate(1/60, output_dir=output_dir, save_range=(0, 60*8))


def scene_2_2():

    x, y = 1960 / 2, 1080 / 2
    rhombus_list = []
    fun_q = lambda t: 400
    fun_p2 = lambda t: -sin((t * pi)) * 90. + 200
    fun_p = lambda t: (sin((t * pi))) * 90. + 300

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


    class ParamFun:

        def __init__(self, d):
            self.d = d

        def __call__(self, *args, **kwargs):
            t = args[0]
            return (sin((t * pi) + (int(self.d/200) * (pi / 16)))) * 90. + 300

    for i, (x_r, y_r) in enumerate(pos):
        dist_from_center = sqrt((x_r - x)**2 + (y_r - y)**2)
        if i < 16:
            fp = lambda t: 200
            fp = lambda  t: -sin((t * pi)) * 90. + 200
            fq = lambda t: 400
        else:
            fp = ParamFun(dist_from_center)
            fq = lambda t: 400

        if i < 16:
            colorset = chinskie
        else:
            #colorset = blue_crystal_vienna
            #colorset = random.sample(chinskie, len(chinskie))
            #print(dist_from_center, dist_from_center/400,int(dist_from_center/400))
            colorset = rotate(chinskie, int(dist_from_center+3)%5)
        rhombus_list.append(RhombusFractal(x_r, y_r, fp, fq, colorset))

    s = Scene(rhombus_list, bg_color=chinskie[1], img_size=(1920, 1080))
    output_dir = 'out/movie_2/scene_2_9'
    #output_dir = None

    f = create_smooth_transition_fun(0.15, 0.15, 0., 4.)
    ft_scale = lambda t: (f(t), (x, y))
    for r in rhombus_list:
        r.scale_time_fun = ft_scale

    files = glob.glob('{}/*'.format(output_dir))

    if output_dir:
        for f in files:
            os.remove(f)
    s.animate(1 / 60, output_dir=output_dir, save_range=(0, 60 * 8))

if __name__ == '__main__':
    scene_2_2()