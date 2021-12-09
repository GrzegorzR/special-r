from math import pi, sin, cos
import pygame.freetype

from special_r.Scene import Scene
from special_r.pyramid.Pyramid import PyramidMoving
from special_r.pyramid.StockPyramidsDrawer import StockPyramidsDrawer
from special_r.utils.colorsets import *
from special_r.utils.parametric_functions import ParametricSegment

pygame.freetype.init()

def main():
    out_dir = 'out/change_s_test'
    out_dir = None
    colors = vienna_wom
    w, h = 200, 200
    height = 15
    dt = 0.1
    scale = 0.86
    steps = 16 * pi / dt
    # print(steps, dt)
    x = 400
    y = 400
    fun = ParametricSegment()
    fun = lambda t: (sin(t / 10.) / 5., 0)
    colors =white_to_red(15)
    pyramides = []



    for x in range(2):
        for y in range(2):
            fun = lambda t: (sin((x+1) / 10.) / 5., 0)
            p = PyramidMoving(200*x+ 200, 200*y+ 200, w, h, fun, colors, scale=scale, border=0)
            p.scale_fun = lambda t: 0.6 + sin(t/10) / 5.




            pyramides.append(p)

    s = Scene([StockPyramidsDrawer(pyramides)], bg_color=colors[0])
    s.animate(dt, output_dir=out_dir, save_range=(0, 900000))


if __name__ == '__main__':
    main()