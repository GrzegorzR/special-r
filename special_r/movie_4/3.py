import os

import drawSvg as draw
from special_r.svg.Transformation import *
from special_r.svg.shapes import *
from special_r.svg.Transformation import *
from special_r.svg.Element import Element, Motif


f_svg = draw.Text('G', 100 , 0, 0)


def main():
    def animate_order(order_n, element, x_p, y_p, out_dir):
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        iters = 1000
        elem_1 = Element(f_svg)
        translations = []
        rotations = []
        rot = Rotation(360./iters, x_p, y_p)
        elements = []
        for i in range(iters):
            print(i)
            sur = draw.Drawing(1920, 1080, origin='center', displayInline=False)
            sur.append(draw.Rectangle(-1920 / 2, -1080 / 2, 1920, 1080, fill='#A9BBC6'))
            sur.append(draw.Circle(rot.x, rot.y, 5, fill="#8C0303"))

            for n in range(order_n):
                if i/iters >= n/order_n:
                    e = Rotation((n/order_n)*360., x_p, y_p)(elem_1)
                    e.draw(sur)

            elem = Rotation((360./iters)*i, x_p, y_p)(elem_1)
            elem.draw(sur)

            sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))


    animate_order(3, f_svg, 0, 0, 'out/3/1')





if __name__ == '__main__':
    main()