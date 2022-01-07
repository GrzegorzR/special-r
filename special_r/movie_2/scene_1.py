import glob
import os
from math import cos, sin, pi

from special_r.Scene import Scene
from special_r.movie_2.movie_2_objects import RhombusFractal
from special_r.utils.colorsets import chinskie


def get_rhombus_tiling_positions(x, y):
    pos = [
        (x, y - 600),

        (x + 200, y - 400),
        (x - 200, y - 400),

        (x - 400, y - 200),
        (x, y - 200),
        (x + 400, y - 200),

        (x - 600, y),
        (x - 200, y),
        (x + 200, y),
        (x + 600, y),

        (x - 400, y + 200),
        (x, y + 200),
        (x + 400, y + 200),

        (x + 200, y + 400),
        (x - 200, y + 400),

        (x, y + 600)]
    return pos


def scene_1():
    colorset = chinskie
    # colorset = schiele_1
    # random.shuffle(colorset)
    # r = Rhombus(200, 200, 100, 200)
    x, y = 1960 / 2, 1080 / 2
    rhombus_list = []
    fun_q = lambda t: 400
    fun_p2 = lambda t: cos((t * pi / 4)) * 90. + 200
    # fun_p2 = lambda t: pow(2, cos(t / 2 + (pi / 2.))) * 90. + 308
    fun_p = lambda t: (sin((t * pi / 2))) * 90. + 300

    pos = get_rhombus_tiling_positions(x, y)
    # fun_reverse_in = [1,2,7,8,9,10]
    border_squares = [0,1,2,3,5,6,9,10,12,13,14,15]
    inside_squares = 4,7,8,11
    for i, (x_r, y_r) in enumerate(pos):
        if i in inside_squares:
            fp, fq = fun_p2, fun_q
        else:
            fp, fq = fun_p, fun_q
        rhombus_list.append(RhombusFractal(x_r, y_r, fp, fq, colorset))

    # r4 = RhombusFractal(400+300/4, 400, (300/2.)*(3./5.), 300/2, colorset)
    # s = Scene([r1,r2,r3, r4], bg_color=colorset[0])
    s = Scene(rhombus_list, bg_color=colorset[1], img_size=(1920, 1080))
    output_dir = 'out/movie_2/scene_1'


    output_dir = None
    files = glob.glob('{}/*'.format(output_dir))

    if output_dir:
        for f in files:
            os.remove(f)
    s.animate(0.01, output_dir=output_dir, save_range=(0, 40 * 50))


if __name__ == '__main__':
    scene_1()
