import os

import drawSvg as draw
from special_r.svg.Transformation import *
from special_r.svg.shapes import *
from special_r.svg.Transformation import *
from special_r.svg.Element import Element, Motif


G_svg = draw.Text('G', 250 , 0, 0, style='font-family:sans serif')
R_svg = draw.Text('R', 500 , 0, 0)
#W, H = 1920, 1080
W, H =  1920, 1080




def animate_order(order_n, svg_elem, x_p, y_p, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    iters = 240
    elem_1 = Element(svg_elem)
    rot = Rotation(360./iters, x_p, y_p)

    for i in range(iters):
        print(i)
        sur = draw.Drawing(W, H, origin='center', displayInline=False)
        #sur.g(style="font-family:sans serif;")
        sur.append(draw.Rectangle(-W/2, -H/2, W, H, fill='#A9BBC6'))
        sur.append(draw.Circle(x_p, y_p, 5, fill="#8C0303"))
        for n in range(order_n):
            if i/iters >= n/order_n:
                e = Rotation((n/order_n)*360., x_p, y_p)(elem_1)
                e.draw(sur)
        elem = Rotation((360./iters)*i, x_p, y_p)(elem_1)
        elem.draw(sur)
        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
        #sur.saveSvg(os.path.join(out_dir, '{}.svg'.format(str(i).zfill(4))))

def vertical_scene():

    out_dir = 'out/3/1'
    animate_order(7, R_svg, 0, 0, out_dir)


def movie_scene():
    tmp_dir = 'out/3/movie_scene/1'
    s = 200
    x,y = s/5.297, s/-3.013
    input_svg = draw.Text('G', s, 0, 0, fill='black')

    animate_order(6, input_svg, x, y, tmp_dir)

def scene_3():

    #elem_1 = Element(G_svg)
    transforms = [Rotation(120*i, 0,0) for i in range(3)]
    #m = Motif(elem_1, transforms)

    animate_order(6, line_svg, -10, 100, 'out/3/line')

if __name__ == '__main__':
    #movie_scene()s\
    scene_3()