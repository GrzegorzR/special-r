import os
from math import sin, cos
import drawSvg as draw
from special_r.svg.Transformation import *
from special_r.svg.shapes import *
from special_r.svg.Transformation import *
from special_r.svg.Element import Element, Motif


f_svg = draw.Text('G', 80 , 0, 0)
k_svg = draw.Text('k', 70 , 0, 0)
x_svg = draw.Text('xD', 50 , 0, 0)


def draw_order(sur, element, order_n, angle, x, y, x_p, y_p):
    iters = 1000
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


def main(out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)


    x_p, y_p = 0, 0
    iters = 1000
    for i in range(iters):
        a = i * (360./1000)
        print(i, sin(i/100)*20.)
        sur = draw.Drawing(1920, 1080, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-1920 / 2, -1080 / 2, 1920, 1080, fill='#A9BBC6'))
        draw_order(sur, f_svg, 6, 360., 0, 0, sin(i/100.)*40., cos(i/100.)*40.)



        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
        #sur.append(draw.Circle(rot.x, rot.y, 5, fill="#8C0303"))

def main_2(out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    iters = 1000
    for i in range(iters):

        sur = draw.Drawing(1920, 1080, origin='center', displayInline=False)

        sur.append(draw.Rectangle(-1920 / 2, -1080 / 2, 1920, 1080, fill='#A9BBC6'))
        print(i)
        #for x in range(-4, 4):
        #    for y in range(-4,4):
#
        #        sur = draw.Drawing(1920, 1080, origin='center', displayInline=False)
        #        sur.append(draw.Rectangle(-1920 / 2, -1080 / 2, 1920, 1080, fill='#A9BBC6'))
        #        draw_order(sur, f_svg, 6, 360., x, y, sin(i/100.)*40., cos(i/100.)*40.)
#
        #        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
                #sur.append(draw.Circle(rot.x, rot.y, 5, fill="#8C0303"))
        for x in range(-3, 4):
            for y in range(-2,2):
                draw_order(sur, f_svg, 6, 360., x*300, y*300 +50, sin(i/100.)*40. + x*10, cos(i/100.)*40. + y*10)
            #draw_order(sur, f_svg, 6, 360., -200, 0, sin(i/100.)*40., cos(i/100.)*40.)

        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))

if __name__ == '__main__':
    out_dir = 'out/5/5'
    #main(out_dir)
    main_2(out_dir)


