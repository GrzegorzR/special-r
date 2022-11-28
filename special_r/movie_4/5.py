import os
from math import sin, cos, pi
import numpy as np
import drawSvg as draw
from special_r.svg.Transformation import *
from special_r.svg.shapes import *
from special_r.svg.Transformation import *
from special_r.svg.Element import Element, Motif

g_svg = draw.Text('G', 60, 0, 0)
k_svg = draw.Text('Kx', 100, 0, 0)
x_svg = draw.Text('<>', 50, 0, 0)
R_svg = draw.Text('R', 500, 0, 0)
#W, H = 1920, 1080
W, H = 1080, 1920

def draw_order(sur, element, order_n, angle, x, y, x_p, y_p):
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
            sur.append(draw.Circle(x + x_p, -y - y_p, 5, fill="#8C0303"))


def scene_5(out_dir, input_svg, pos_t_fun, iters=2000, dt=0.005):
    x_dif = 300

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for i in range(iters):
        if not i % 50:
            print(i, sin(i / 100) * 20.)
        sur = draw.Drawing(1920, 1080, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-1920 / 2, -1080 / 2, 1920, 1080, fill='#A9BBC6'))
        # draw_order(sur, input_svg, 6, 360., -sin(i*dt)*40.+x_dif,  -cos(i*dt)*40., sin(i*dt)*40., cos(i*dt)*40.)
        # draw_order(sur, input_svg, 6, 360., -x_dif, 0, sin(i *dt) * 40., cos(i *dt) * 40.)
        x_p, y_p = pos_t_fun(i * dt)
        draw_order(sur, input_svg, 6, 360., x_dif - x_p, -y_p, x_p, y_p)
        draw_order(sur, input_svg, 6, 360., -x_dif, 0, x_p, y_p)

        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
        # sur.append(draw.Circle(rot.x, rot.y, 5, fill="#8C0303"))

def scene_5_vertical(out_dir, input_svg, pos_t_fun, iters=2000, dt=0.005):
    x_dif = 300

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for i in range(iters):
        if not i % 50:
            print(i, sin(i / 100) * 20.)
        sur = draw.Drawing(W, H, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))

        x_p, y_p = pos_t_fun(i * dt)
        x_p, y_p = x_p*2, y_p*2
        draw_order(sur, input_svg, 7, 360., 0, 0, x_p, y_p)
        #draw_order(sur, input_svg, 6, 360., -x_dif, 0, x_p, y_p)

        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
        # sur.append(draw.Circle(rot.x, rot.y, 5, fill="#8C0303"))


def scene_vertical_out(out_dir, iters):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    x_p, y_p = 0, 0

    out_range = np.linspace(500, 60, iters)

    for i in range(iters):
        print(i)
        sur = draw.Drawing(W, H, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))
        sur.append(draw.Circle(x_p, y_p, 5, fill="#8C0303"))
        tmp_svg = draw.Text('R', out_range[i], 0, 0)
        draw_order(sur, tmp_svg, 7, 360., 0, 0, x_p, y_p)
        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))


if __name__ == '__main__':
    out_dir = 'out/5/vertical'
    dt = pi/120.
    iters = 480
    element = k_svg

    fun_only_x = lambda t: (sin(t) * 40., 0.)
    fun_circle = lambda t: (sin(t) * 40., (cos(t) * 40) - 40)
    fun_3 = lambda t: (sin(t*2) * 80., (cos(4 * t) * cos(2 * t) * 40) -40)


    a, b, fi = 2., 3., pi/2.
    A, B  = 40, 40
    fun_4 = lambda t: (sin(a*t + fi) * A, (B*(sin(t*b)) - 40))

    #scene_5('out/5/1', element, fun_only_x, iters, dt)
    #scene_5('out/5/2', element, fun_circle, iters, dt)
    #scene_5('out/5/6', element, fun_4, iters, dt)
    scene_5_vertical('out/5/vertical', R_svg, fun_circle, iters, dt)
    scene_vertical_out('out/5/vertical_out', 120)