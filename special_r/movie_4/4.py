import os

import drawSvg as draw
from special_r.svg.Transformation import *
from special_r.svg.shapes import *
from special_r.svg.Transformation import *
from special_r.svg.Element import Element, Motif


f_svg = draw.Text('G', 100 , 0, 0)
k_svg = draw.Text('k', 70 , 0, 0)
x_svg = draw.Text('xD', 50 , 0, 0)

def main(out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    def draw_order(sur, element, order_n, angle,  x, y, x_p, y_p):
        iters = 1000
        elem_1 = Element(element)

        angle_step = 360./order_n
        e = Rotation(angle, x_p, y_p)(elem_1)
        e = Translation(x, y)(e)
        e.draw(sur)
        for n in range(order_n):
            if angle >= n*angle_step:
                e = Rotation((n / order_n) * 360., x_p, y_p)(elem_1)
                e = Translation(x, y)(e)
                e.draw(sur)
                sur.append(draw.Circle(x-x_p, -y-y_p, 5, fill="#8C0303"))
    x_p, y_p = 0, 0
    iters = 1000
    for i in range(iters):
        a = i * (360./1000)
        print(i)
        sur = draw.Drawing(1920, 1080, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-1920 / 2, -1080 / 2, 1920, 1080, fill='#A9BBC6'))
        draw_order(sur, f_svg, 2, a, -800, 0, x_p, y_p)
        draw_order(sur, f_svg, 3, a, -600, 0, x_p, y_p)
        draw_order(sur, f_svg, 4, a, -400, 0, x_p, y_p)
        draw_order(sur, f_svg, 5, a, -200, 0, x_p, y_p)
        draw_order(sur, f_svg, 6, a, 0, 0, x_p, y_p)
        draw_order(sur, f_svg, 7, a, 200, 0, x_p, y_p)
        draw_order(sur, f_svg, 8, a, 400, 0, x_p, y_p)
        draw_order(sur, f_svg, 9, a, 600, 0, x_p, y_p)

        draw_order(sur, k_svg, 2, a, -800, 300, x_p, y_p)
        draw_order(sur, k_svg, 3, a, -600, 300, x_p, y_p)
        draw_order(sur, k_svg, 4, a, -400, 300, x_p, y_p)
        draw_order(sur, k_svg, 5, a, -200, 300, x_p, y_p)
        draw_order(sur, k_svg, 6, a, 0, 300, x_p, y_p)
        draw_order(sur, k_svg, 7, a, 200, 300, x_p, y_p)
        draw_order(sur, k_svg, 8, a, 400, 300, x_p, y_p)
        draw_order(sur, k_svg, 9, a, 600, 300, x_p, y_p)


        draw_order(sur, x_svg, 2, a, -800, -300, x_p, y_p)
        draw_order(sur, x_svg, 3, a, -600, -300, x_p, y_p)
        draw_order(sur, x_svg, 4, a, -400, -300, x_p, y_p)
        draw_order(sur, x_svg, 5, a, -200, -300, x_p, y_p)
        draw_order(sur, x_svg, 6, a, 0, -300, x_p, y_p)
        draw_order(sur, x_svg, 7, a, 200, -300, x_p, y_p)
        draw_order(sur, x_svg, 8, a, 400, -300, x_p, y_p)
        draw_order(sur, x_svg, 9, a, 600, -300, x_p, y_p)


        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
        #sur.append(draw.Circle(rot.x, rot.y, 5, fill="#8C0303"))









if __name__ == '__main__':
    out_dir = 'out/4/2'
    main(out_dir)