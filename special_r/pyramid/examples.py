from math import pi, sin, cos
from colour import Color

from special_r.Scene import Scene
from special_r.pyramid.Pyramid import Pyramid, PyramidMoving
from special_r.pyramid.StockPyramidsDrawer import StockPyramidsDrawer
from special_r.pyramid.Tiling import TilingRects
from special_r.utils.colorsets import blue_crystal_vienna, schiele_1, mech_keyboard, vienna_wom, vienna_strips
from special_r.utils.parametric_functions import ParametricCircle, LissajousCurve, ParametricSegment


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
    out_dir = None
    c = list(reversed(schiele_1))
    w, h = 200, 200
    pyramides = []

    dt = 0.08
    steps = 16 * pi / dt
    print(steps, dt)

    for x in range(0, 4):
        for y in range(0, 4):
            clockwise = False
            phase = pi * x / 8 + pi * y / 8

            if x > 1 and y < 2:
                clockwise = False

            if x > 1 and y > 1:
                clockwise = False

            p = PyramidMoving(150 + x * 200, 150 + y * 200, w, h, ParametricCircle(clockwise, phase),
                              colors=c, scale=0.75, height=13, borders_colors=c)
            pyramides.append(p)

    o = StockPyramidsDrawer(pyramides)
    s = Scene([o], bg_color=c[0], img_size=(1080, 1920))
    s.animate(dt, output_dir=out_dir, save_range=(0, steps))


def part_5():
    out_dir = 'out/pym_6'
    out_dir = None
    # c = nikifor_1
    c = mech_keyboard
    w, h = 200, 200
    pyramides = []

    dt = 0.01
    steps = 16 * pi / dt
    # print(steps, dt)
    x = 400
    y = 400
    fun1 = ParametricCircle(clockwise=True)
    fun = LissajousCurve(3., 2.6)

    p = PyramidMoving(x, y, w, h, fun, colors=c, scale=0.88, anim_param=4, height=21)

    pyramides.append(p)

    o = StockPyramidsDrawer(pyramides)
    s = Scene([o], bg_color=c[2])
    s.animate(dt, output_dir=out_dir, save_range=(0, steps))


def part_6():
    out_dir = 'out/pym_6'
    out_dir = None
    # c = nikifor_1
    c = vienna_wom
    # c = vienna_strips
    w, h = 200, 200
    pyramides = []

    dt = 0.2
    steps = 16 * pi / dt
    # print(steps, dt)
    x = 400
    y = 400
    fun = ParametricSegment()

    p = PyramidMoving(x, y, w, h, fun, colors=c, scale=0.8, anim_param=10, height=10)

    pyramides.append(p)

    o = StockPyramidsDrawer(pyramides)
    s = Scene([o], bg_color=c[1])
    s.animate(dt, output_dir=out_dir, save_range=(0, steps))


def tiling_1(out_dir, funs, colorsets, dt=0.04, border_size=2):
    steps = 8 * pi / dt
    img_size = (900, 900)

    small = 300, 300
    big_h = 300, 600
    big_w = 600, 300
    sizes = [big_w,
             small,
             small,
             small,
             big_h,
             small,
             small]
    positions = [
        (300, 150),
        (750, 150),
        (150, 450),
        (450, 450),
        (750, 600),
        (150, 750),
        (450, 750),
    ]

    pyms = []

    for i in range(len(positions)):
        pyms.append(
            PyramidMoving(positions[i][0], positions[i][1],
                          sizes[i][0], sizes[i][1],
                          funs[i], colors=colorsets[i],
                          scale=0.8, anim_param=20, height=10, border=border_size)
        )

    p = StockPyramidsDrawer(pyms)
    s = Scene([p], bg_color=(0, 0, 0), img_size=img_size)
    s.animate(dt, output_dir=out_dir, save_range=(0, steps))


def part_7():
    out_dir = 'out/pym_7_7'
    out_dir = None
    img_size = (900, 900)

    funs = [
        ParametricSegment(),
        LissajousCurve(),
        ParametricSegment(),
        ParametricCircle(True),
        ParametricSegment(),
        LissajousCurve(4, 3, -4, -4),
        ParametricSegment(),
    ]
    colorsets = [
        vienna_wom,
        vienna_strips,
        vienna_strips,
        vienna_wom,
        vienna_wom,
        vienna_wom,
        vienna_strips

    ]

    tiling_1(out_dir, funs, colorsets)


def part_8():
    out_dir = 'out/pym_14'
    out_dir = None

    dt = 0.04

    img_size = (900, 900)

    small = 300, 300
    big_h = 300, 600
    big_w = 600, 300
    sizes = [big_w,
             small,
             small,

             (300, 150),
             (300, 150),

             big_h,
             small,
             small]
    positions = [
        (300, 150),
        (750, 150),
        (150, 450),

        (450, 375),
        (450, 525),

        (750, 600),
        (150, 750),
        (450, 750),
    ]

    def two_colors(col1, col2, height):
        return [col1 for _ in range(height - 1)] + [col2]

    r_speed, phase = 1., pi / 4.

    def fun1(t):
        return 2*sin(r_speed * t + phase), 2*cos(r_speed * t + phase) * cos(r_speed * t + phase)

    def fun2(t):
        x, y = fun1(t)
        return -x, -y

    funs = [fun1 for _ in range(3)]
    funs = funs + [ParametricSegment(2.5),
                   ParametricSegment(-2.5)
                   ]
    funs = funs + [fun2 for _ in range(3)]

    funs = [ParametricSegment(1) for _ in range(3)]
    funs = funs + [fun1, fun2]
    funs = funs + [ParametricSegment(-1) for _ in range(3)]

    colors = [two_colors((255, 255, 255), '#D0362D', len(positions)) for _ in range(4)]

    red = Color('red')
    white = Color('white')
    green = Color('green')
    white_to_red = [c.hex_l.upper() for c in white.range_to(red, 10)]
    white_to_green = [c.hex_l.upper() for c in white.range_to(green, 10)]
    colors = [white_to_red for _ in range(4)] + [white_to_green for _ in range(4)]
    # colors += list(red.range_to(Color("blue").rgb, 4))
    # colors = colors + [two_colors((255, 255, 255), (12, 55, 10), len(positions)) for _ in range(4)]
    # colors = [vienna_wom for i in range(4)]
    # colors = colors+[vienna_strips for i in range(4)]

    t = TilingRects(sizes, positions, funs, colors, img_size)

    t.animate(dt, out_dir)


if __name__ == '__main__':
    part_3()
