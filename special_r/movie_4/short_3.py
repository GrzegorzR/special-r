import copy
import os
import random
import string
from math import sin, pi

from planar import Vec2, Affine
import drawSvg as draw
import numpy as np

from special_r.svg.Transformation import *
from special_r.svg.shapes import *
from special_r.svg.Transformation import *
from special_r.svg.Element import Element, Motif, ElementContainer

t_svg_150 = draw.Text('t', 150, 0, 0, fill=None)

t_svg = draw.Text('t', 60, 0, 0, fill=None)

# W, H = 1920, 1080
W, H = 1080 , 1920
main_iterator = 0


def rotate(p, origin=(0, 0), degrees=0):
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle), np.cos(angle)]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    res = np.squeeze((R @ (p.T - o.T) + o.T).T)
    dif = p - res
    return np.around(np.array([res[0], p[0][1] - dif[0][1]]), 0)


def animate_order(input_element, i, iters_num, order_n, x_p, y_p, sur):
    angle = (360. / iters_num) * i

    result = []
    for n in range(1, order_n):
        # print(i/iters_num, n/order_n, i/iters_num >= n/order_n)
        if i / iters_num >= n / order_n:
            e = Rotation((n / order_n) * 360., x_p, y_p)(input_element)
            e.draw(sur)

            result.append(e)

    e = Rotation(angle, x_p, y_p)(input_element)
    e.draw(sur)
    return result


def scene_char_select(out_dir):
    os.makedirs(out_dir, exist_ok=True)

    sample = random.sample(string.printable[:-10], 11)
    print(sample)
    sample.append('t')
    iterator = 0
    t_x = 87.5
    for c in sample:
        sur = draw.Drawing(W, H, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))
        svg_150 = draw.Text(c, 150, 0, 0, fill=None)
        element = Element(svg_150)
        element = Translation(-t_x / 2, 0)(element)
        element.draw(sur)
        for i in range(20):
            sur.savePng(os.path.join(out_dir, '{}.png'.format(str(iterator).zfill(4))))
            iterator += 1


def scene_reflect(input_svg, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    t_x = 87.5
    iters = 120

    parameter_x = np.linspace(1, -1, iters)
    parameter_tx = np.linspace(0, t_x, iters)
    for i in range(iters):
        ix = parameter_x[i]
        it_x = parameter_tx[i]
        e = Element(input_svg)
        sur = draw.Drawing(W, H, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))

        t = TransChain([Translation(it_x, 0), CustomTransformation([[ix, 0, 0],
                                                                   [0, 1, 0]])])
        e2 = t(e)
        elemns = ElementContainer([e, e2])
        elemns = Translation(-t_x / 2, 0)(elemns)
        elemns.draw(sur)
        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
        #sur.saveSvg(os.path.join(out_dir, '{}.svg'.format(str(i).zfill(4))))


def vid_1(input_svg, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    for i in range(360):
        t = (i * 2 * pi) / 240.

        e = Element(input_svg)
        t_x = (sin(t) + 1.75) * 50
        sur = draw.Drawing(W, H, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))
        print(i, t_x)
        t = TransChain([Translation(t_x, 0), ReflectX()])
        e2 = t(e)
        elemns = ElementContainer([e, e2])
        elemns = Translation(-t_x / 2, 0)(elemns)
        elemns.draw(sur)
        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
        # sur.saveSvg(os.path.join(out_dir,'tes4.svg'))


def vid_2(input_svg, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    t_x = 87.5
    x_p, y_p = 0, 50
    iters = 240
    for i in range(iters + 1):
        e = Element(input_svg)
        sur = draw.Drawing(W, H, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))
        sur.append(draw.Circle(x_p, -y_p, 5, fill="#8C0303"))
        t = TransChain([Translation(t_x, 0), ReflectX()])
        e2 = t(e)
        elemns = ElementContainer([e, e2])
        elemns = Translation(-t_x / 2, 0)(elemns)
        elemns.draw(sur)
        animate_order(elemns, i, iters, 9, x_p, y_p, sur)
        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))


def vid_3(input_svg, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    t_x = 75
    iters = 240

    x_p, y_p = 0, 50
    for i in range(480):
        print(i)
        t = (i * 2 * pi) / 240.

        e = Element(input_svg)
        t_x = (sin(t) + 1.75) * 50
        print(t_x)
        sur = draw.Drawing(W, H, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))
        sur.append(draw.Circle(x_p, -y_p, 5, fill="#8C0303"))
        t = TransChain([Translation(t_x, 0), ReflectX()])
        e2 = t(e)
        elemns = ElementContainer([e, e2])
        elemns = Translation(-t_x / 2, 0)(elemns)
        animate_order(elemns, 12, 12, 9, x_p, y_p, sur)
        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))


def get_rosseta_elems(input_element, x, y, order_n, x_p, y_p, t_x):
    elem = Element(input_element)
    t = TransChain([Translation(t_x, 0), ReflectX()])
    e2 = t(elem)
    elemns = ElementContainer([elem, e2])
    elemns = Translation(-t_x / 2, 0)(elemns)
    elemns = Translation(x, y)(elemns)
    result = []
    for n in range(0, order_n):
        e = Rotation((n / order_n) * 360., x_p + x, y_p + y)(elemns)
        result.append(e)

    return result

def draw_rosseta(sur, input_element, x, y, order_n, x_p, y_p, t_x):
    elements = get_rosseta_elems(input_element, x, y, order_n, x_p, y_p, t_x)
    for e in elements:
        e.draw(sur)

def scene_scale_out(input_svg, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    t_x = 87.5
    x_p, y_p = 0, 50
    iters = 60
    rosetta_elem = get_rosseta_elems(input_svg, 0, 0, 9, x_p, y_p, t_x)
    scale_gradient = np.linspace(1,0.4, iters)
    for i in range(iters):
        sur = draw.Drawing(W, H, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))
        e = Scale(scale_gradient[i])(rosetta_elem)
        e.draw(sur)
        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))

def vid_4(input_svg, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    e = input_svg
    iters = 600

    def iteration_filter(i, i_max):
        if i >= i_max:
            return 1.
        else:
            return i / i_max

    for i in range(iters):
        print(i)
        t = (i * 2 * pi) / 240.
        sur = draw.Drawing(W, H, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))
        for y in range(-410, 370, 150):

            t_x = (sin(t + ((y / 100) + 4) * (pi / 6)) + 1.75) * 50 * iteration_filter(i, 240)
            t_x2 = (sin(t + ((y / 100) + 4) * (pi / 6) + (pi/4)) + 1.75) * 50 * iteration_filter(i, 240)
            t_x3 = (sin(t + ((y / 100) + 4) * (pi / 6) - (pi/4)) + 1.75) * 50 * iteration_filter(i, 240)
            draw_rosseta(sur, e, -200, y, 9, 0, 0, t_x2)
            draw_rosseta(sur, e, 0, y, 9, 0, 0, t_x)
            draw_rosseta(sur, e, 200, y, 9, 0, 0, t_x3)
            sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))


if __name__ == '__main__':
    scene_char_select('out/short_3_2/1')
    scene_reflect(t_svg_150, 'out/short_3_2/2')
    vid_1(t_svg, 'out/short_3_2/3')
    vid_2(t_svg_150, 'out/short_3_2/4')
    scene_scale_out(t_svg_150, 'out/short_3_2/5')
    vid_3(t_svg_150, 'out/short_3_2/6')
    vid_4(t_svg, 'out/short_3_2/7')
