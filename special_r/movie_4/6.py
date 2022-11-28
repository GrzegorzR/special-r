import os
from math import sin, cos, pi, exp
import numpy as np
import drawSvg as draw
from special_r.svg.Transformation import *
from special_r.svg.shapes import *
from special_r.svg.Transformation import *
from special_r.svg.Element import Element, Motif
import matplotlib.pyplot as plt

g_svg = draw.Text('G', 60, 0, 0)
k_svg = draw.Text('kr', 40, 0, 0)
x_svg = draw.Text('<>', 50, 0, 0)
R_svg = draw.Text('R', 60, 0, 0)


def draw_order(sur, element, order_n, angle, x, y, x_p, y_p, center_circle=True):
    elem_1 = Element(element)

    angle_step = 360. / order_n
    e = Rotation(angle, x_p, y_p)(elem_1)
    e = Translation(x, y)(e)
    e.draw(sur)
    for n in range(order_n):
        if angle >= n * angle_step:
            e = Rotation((n / order_n) * 360., x_p, y_p)(elem_1)
            e = Translation(x, y)(e)
            e.draw(sur)
            if center_circle:
                sur.append(draw.Circle(x + x_p, -y - y_p, 5, fill="#8C0303"))


def main(out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    x_p, y_p = 0, 0
    iters = 1000
    for i in range(iters):
        # a = i * (360./1000)
        # print(i, sin(i/100)*20.)
        sur = draw.Drawing(1920, 1080, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-1920 / 2, -1080 / 2, 1920, 1080, fill='#A9BBC6'))
        draw_order(sur, f_svg, 6, 360., 0, 0, sin(i / 100.) * 40., cos(i / 100.) * 40.)

        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
        # sur.append(draw.Circle(rot.x, rot.y, 5, fill="#8C0303"))


def main_2(out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    iters = 1000
    for i in range(iters):

        sur = draw.Drawing(1920, 1080, origin='center', displayInline=False)

        sur.append(draw.Rectangle(-1920 / 2, -1080 / 2, 1920, 1080, fill='#A9BBC6'))
        print(i)
        # for x in range(-4, 4):
        #    for y in range(-4,4):
        #
        #        sur = draw.Drawing(1920, 1080, origin='center', displayInline=False)
        #        sur.append(draw.Rectangle(-1920 / 2, -1080 / 2, 1920, 1080, fill='#A9BBC6'))
        #        draw_order(sur, f_svg, 6, 360., x, y, sin(i/100.)*40., cos(i/100.)*40.)
        #
        #        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
        # sur.append(draw.Circle(rot.x, rot.y, 5, fill="#8C0303"))
        for x in range(-3, 4):
            for y in range(-2, 2):
                draw_order(sur, f_svg, 6, 360., x * 300, y * 300 + 50, sin(i / 100.) * 40. + x * 10,
                           cos(i / 100.) * 40. + y * 10)
            # draw_order(sur, f_svg, 6, 360., -200, 0, sin(i/100.)*40., cos(i/100.)*40.)

        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))


def main_3(out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    x_max, y_max = 1920, 1080
    dt = pi / 500.
    iters = 1901
    for i in range(1850, iters):
        print(i)
        sur = draw.Drawing(x_max, y_max, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-1920 / 2, -1080 / 2, 1920, 1080, fill='#A9BBC6'))

        for x in range(-8, 9):
            for y in range(-4, 5):
                x_c, y_c = x * 100, y * 100
                x_a, y_a = ((x_c + x_max / 2.) / x_max) * 2. * pi, ((y_c + y_max / 2.) / y_max) * 2. * pi
                x_p, y_p = sin(dt * i + x_a) * 20., cos(dt * i + y_a) * 20.
                draw_order(sur, g_svg, 6, 360.,
                           x_c - x_p, y_c - y_p, x_p, y_p, center_circle=False)
        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
    for i in range(iters, iters + 60):
        print(i)
        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
    sur.saveSvg(os.path.join('out', '{}.svg'.format(str(iters))))


def main_4(out_dir):
    from scipy import signal
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    def cor_fun(x, b, c=250.):
        g_val = exp(-((x - b) ** 2) / (2. * c ** 2))
        d = 60
        x_p, y_p = d * g_val - d / 3, d * g_val - d / 3
        return x_p, y_p

    x_max, y_max = 1920, 1080
    dt = pi / 1000.
    iters = 240
    for i in range(iters):
        print(i)
        t = dt * i
        sur = draw.Drawing(x_max, y_max, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-1920 / 2, -1080 / 2, 1920, 1080, fill='#A9BBC6'))

        # print(saw_v)
        for x in range(-8, 9):
            for y in range(-4, 5):
                x_c, y_c = x * 100, y * 100
                # x_a, y_a = ((x_c+x_max/2.)/x_max)*2.*pi,((y_c+y_max/2.)/y_max)*2.*pi
                tt = t + y * dt * 15
                saw_v = signal.sawtooth(np.pi * 5 * tt) * x_max * 1.25
                x_p, y_p = cor_fun(x_c, saw_v)

                # x_p, y_p = sin(dt*i + x_a)*20.,  cos(dt*i + y_a)*20.
                draw_order(sur, g_svg, 6, 360.,
                           x_c - x_p, y_c - y_p, x_p, y_p, center_circle=False)
        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
    for i in range(iters, iters + 60):
        print(i)
        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
    sur.saveSvg(os.path.join('out', '{}.svg'.format(str(iters))))


def main_5(out_dir, ):
    from scipy import signal
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    svg_element = k_svg

    def cor_fun(x, b, c=200.):
        g_val = exp(-((x - b) ** 2) / (2. * c ** 2))
        d = 60
        x_p, y_p = d * g_val - d / 3, d * g_val - d / 3
        return x_p, y_p

    x_max, y_max = 1080, 1920
    dt = pi / 1000.
    iters = 24
    dd = []

    for i in range(iters):
        print(i)
        t = dt * i
        sur = draw.Drawing(x_max, y_max, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-1080 / 2, -1920 / 2, 1080, 1920, fill='#A9BBC6'))

        # print(saw_v)

        for x in range(-4, 5):
            for y in range(-4, 5):
                x_c, y_c = x * 100, y * 100
                # x_a, y_a = ((x_c+x_max/2.)/x_max)*2.*pi,((y_c+y_max/2.)/y_max)*2.*pi
                tt = t + y * dt * 20
                saw_v = signal.sawtooth(np.pi * 5 * tt) * x_max * 1.25
                dd.append(saw_v)
                # plt.plot(sa)
                # print(saw_v)
                x_p, y_p = cor_fun(x_c, saw_v)

                # x_p, y_p = sin(dt*i + x_a)*20.,  cos(dt*i + y_a)*20.
                draw_order(sur, svg_element, 6, 360.,
                           x_c - x_p, y_c - y_p, x_p, y_p, center_circle=False)
        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))


def main_6():
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    x_max, y_max = 1920, 1080
    dt = pi / 500.
    iters = 4000
    for i in range(3369, iters):
        print(i)
        sur = draw.Drawing(x_max, y_max, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-1920 / 2, -1080 / 2, 1920, 1080, fill='#A9BBC6'))

        for x in range(-8, 9):
            for y in range(-4, 5):
                x_c, y_c = x * 100, y * 100
                x_a, y_a = ((x_c + x_max / 2.) / x_max) * 2. * pi, ((y_c + y_max / 2.) / y_max) * 2. * pi
                x_p, y_p = sin(dt * i + x_a) * 20., cos(dt * i + y_a) * 20.
                draw_order(sur, g_svg, 6, 360.,
                           x_c - x_p, y_c - y_p, x_p, y_p, center_circle=False)
        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))


def vertical_grid(out_dir, svg_element):
    from scipy import signal
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    def cor_fun(x, b, c=250.):
        g_val = exp(-((x - b) ** 2) / (2. * c ** 2))
        d = 40
        x_p, y_p = d * g_val, d * g_val
        return x_p, y_p
        # return 0, 0

    def pow_fun(t):
        max_t = 60
        if t > max_t:
            return 1.
        else:
            return t / (max_t + 1.)

    x_max, y_max = 1080, 1920
    dt = pi / 800.
    iters = 800
    dd = []

    for i in range(iters):
        print(i)
        t = dt * i
        sur = draw.Drawing(x_max, y_max, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-1080 / 2, -1920 / 2, 1080, 1920, fill='#A9BBC6'))

        # print(saw_v)

        for x in range(-4, 5):
            for y in range(-4, 5):
                x_c, y_c = x * 100, y * 100
                tt = t + y * dt * 20
                saw_v = signal.sawtooth(15 * tt) * x_max * 1.25
                dd.append(saw_v)

                x_p, y_p = cor_fun(x_c, saw_v)
                x_p, y_p = x_p * pow_fun(i), y_p * pow_fun(i)
                draw_order(sur, svg_element, 7, 360.,
                           x_c - x_p, y_c - y_p, x_p, y_p, center_circle=False)
        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))


def plots_grid(out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    x_max, y_max = 1920, 1080
    dt = pi / 500.
    for i in range(3800, 3801, 100):
        print(i)
        sur = draw.Drawing(x_max, y_max, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-x_max / 2, -y_max / 2, x_max, y_max, fill='#A9BBC6'))
        for x in range(-8, 9):
            for y in range(-4, 5):
                x_c, y_c = x * 100, y * 100
                x_a, y_a = ((x_c + x_max / 2.) / x_max) * 2. * pi, ((y_c + y_max / 2.) / y_max) * 2. * pi
                x_p, y_p = sin(dt * i + x_a) * 20., cos(dt * i + y_a) * 20.
                if x ==2 and y == 2:
                    print(x_p, y_p)
                    draw_order(sur, g_svg, 6, 360.,
                           x_c - x_p, y_c - y_p, x_p, y_p, center_circle=False)

        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
        sur.saveSvg(os.path.join(out_dir, '{}.svg'.format(str(i).zfill(4))))


if __name__ == '__main__':
    out_dir = 'out/test'
    # main(out_dir)
    plots_grid(out_dir)

    # vertical_grid(out_dir, R_svg)
