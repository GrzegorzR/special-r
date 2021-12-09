from math import pi

from special_r.movie_1.utils import PyramidsScene
from special_r.pyramid.Pyramid import PyramidMoving
from special_r.utils.colorsets import blue_crystal_vienna
from special_r.utils.parametric_functions import ParametricCircle


def get_pyms_scene_2():
    x, y = 1920 / 2, 500
    w, h = 300., 300.
    c = blue_crystal_vienna
    offset = 250
    #
    p2 = PyramidMoving(x - offset, y +offset, w, h, ParametricCircle(True, 0), colors=c, borders_colors=c, scale=0.9, height=13)
    p1 = PyramidMoving(x - offset, y -offset, w, h, ParametricCircle(False, pi), colors=c, borders_colors=c, scale=0.9, height=13)
    p3 = PyramidMoving(x + offset, y +offset, w, h, ParametricCircle(False, 0), colors=c, borders_colors=c, scale=0.9, height=13)
    p4 = PyramidMoving(x + offset, y -offset, w, h, ParametricCircle(True, pi), colors=c, borders_colors=c, scale=0.9, height=13)

    return [p2, p1, p3, p4]


def get_scene_2_obj():
    bg_color = blue_crystal_vienna[0]
    dt = 0.05
    return PyramidsScene(get_pyms_scene_2, 150, dt, bg_color, img_size=(1920, 1080))


if __name__ == '__main__':
    s = get_scene_2_obj()
    s.display()
