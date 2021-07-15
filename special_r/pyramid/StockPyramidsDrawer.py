from special_r.pyramid.Pyramid import Pyramid, PyramidMoving
from special_r.Scene import Scene
from special_r.utils.colorsets import blue_crystal_vienna, schiele_1
from special_r.utils.parametric_functions import *


class StockPyramidsDrawer:
    def __init__(self, pyramids):
        self.pyramids = pyramids
        self.max_l = max([len(p.rects) for p in self.pyramids])

    def update(self, ts):
        for p in self.pyramids:
            p.update(ts)

    def draw(self, surface):
        for i in range(self.max_l):
            for p in self.pyramids:
                if i < len(p.rects):
                    p.rects[i].draw(surface)


def part_1():
    p1 = Pyramid(400, 400, 200, 460, scale=0.8, x_t=0.1, y_t=0.04, height=8, vr=1)
    p2 = Pyramid(300., 300., 500., 200., scale=0.6, x_t=0., height=7, vr=0.3)

    o = StockPyramidsDrawer([p1, p2])
    s = Scene([o])
    s.animate(0)


def part_2():
    out_dir = 'out/pym_2'
    # out_dir = None
    x, y = 500, 500.
    w, h = 200., 200.
    c = blue_crystal_vienna
    #
    p2 = PyramidMoving(x, y, w, h, ParametricCircle(False, 0), colors=c, scale=0.9, height=15)
    p1 = PyramidMoving(x - w, y, w, h, ParametricCircle(True, pi), colors=c, scale=0.9, height=15)
    p3 = PyramidMoving(x - w, y - h, w, h, ParametricCircle(False, pi), colors=c, scale=0.9, height=15)
    p4 = PyramidMoving(x, y - h, w, h, ParametricCircle(True, 0), colors=c, scale=0.9, height=15)
    o = StockPyramidsDrawer([p1, p2, p3, p4])
    s = Scene([o], bg_color=c[0])
    s.animate(output_dir=out_dir)


def part_3():
    out_dir = 'out/pym_4'
    #out_dir = None
    c = list(reversed(schiele_1))
    w, h = 200, 200
    pyramides = []

    dt = 0.08
    steps = 16*pi/dt
    print(steps, dt)


    for x in range(0, 4):
        for y in range(0, 4):
            clockwise = False
            phase = pi*x/8 + pi*y/8

            if x > 1 and y < 2:
                clockwise = False

            if x > 1 and y > 1:
                clockwise = False

            p = PyramidMoving(150 + x * 200, 150 + y * 200, w, h, ParametricCircle(clockwise, phase),
                              colors=c, scale=0.75, height=11)
            pyramides.append(p)

    o = StockPyramidsDrawer(pyramides)
    s = Scene([o], bg_color=c[0])
    s.animate(dt, output_dir=out_dir, save_range=(0, steps))



if __name__ == '__main__':
    part_3()
