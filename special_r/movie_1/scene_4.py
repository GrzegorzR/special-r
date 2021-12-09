import itertools
from math import pi

from special_r.movie_1.utils import PyramidsScene
from special_r.pyramid.Pyramid import PyramidMoving
from special_r.utils.colorsets import *
from special_r.utils.parametric_functions import ParametricCircle, LissajousCurve

c = list(reversed(white_to_green(10)))
def get_square_grid_pos(borders, nums, sizes, img_size):
    border_x, border_y = borders
    num_x, num_y = nums
    size_x, size_y = sizes
    w, h = img_size
    center_x, center_y = w/2, h/2

    out = [[None for _ in range(num_x)] for _ in range(num_y)]
    for x, y in itertools.product(range(num_x), range(num_y)):

        pym_x = border_x + x*((w - 2*border_x )/(num_x-1))
        pym_y = border_y + y * ((h - 2 * border_y) / (num_y - 1))

        out[x][y] = (pym_x, pym_y)
    return out


def get_pyms_scene_4():
    center_x, center_y = 1920 / 2, 1080/2
    w, h = 200., 200.

    num =3
    pyms = []
    positions = get_square_grid_pos((600, 200), (num, num), (100, 100), (1920, 1080))
    for x, y in itertools.product(range(num), range(num)):
        pos_x, pos_y = positions[x][y]
        p = PyramidMoving(pos_x, pos_y, 200+ x*200 , 100 + y*20, LissajousCurve(1,1,1,1), colors=c, borders_colors=c, scale=0.9, height=10)
        pyms.append(p)
    return pyms

def get_scene_4_obj():
    bg_color = c[1]
    dt = 0.2
    return PyramidsScene(get_pyms_scene_4, 300, dt, bg_color, img_size=(1920, 1080))


if __name__ == '__main__':
    s = get_scene_4_obj()
    s.display()