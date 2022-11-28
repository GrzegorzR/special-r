import os.path
from PIL import Image

import drawSvg as draw
from special_r.svg.Transformation import *
from special_r.svg.shapes import *
from special_r.svg.Transformation import *
from special_r.svg.Element import Element, Motif


ch = "»"
ch = 'F'
f_svg =  draw.Text('R', 60 , 0, 0)
W, H = 2000, 2000


def draw_n_ord(n, element, sur, x_p, y_p, x_t, y_t):
        rotations = [TransChain([Rotation(i * (360/n) , x_p, y_p)]) for i in range(0, n)]
        motif = Motif(element, rotations)
        motif = Translation(-x_p, -y_p)(motif)
        motif = Translation(x_t, y_t)(motif)
        motif.draw(sur)

def order_2():
    name = 'order_2_2'

    d = draw.Drawing(900, 900, origin='center', displayInline=False)
    elem = Element(f_svg)
    def draw_2_ord(element, sur, x_p, y_p, x_t, y_t):
        rotations = [TransChain([Rotation(i * 180 , x_p, y_p)]) for i in range(0, 2)]
        motif = Motif(element, rotations)
        motif = Translation(-x_p, -y_p)(motif)
        motif = Translation(x_t, y_t)(motif)
        motif.draw(sur)

    draw_2_ord(elem, d, 38, -81, -300, 0)
    draw_2_ord(elem, d, 5, -55.75, -200, 0)
    draw_2_ord(elem, d, 30, -55.75, -100, 0)
    draw_2_ord(elem, d, 30, -25.75, 0, 0)
    draw_2_ord(elem, d, 17, 0, 100, 0)
    draw_2_ord(elem, d, 35, -55.75, 200, 0)
    draw_2_ord(elem, d, 17, -75, 300, 0)

    d.setRenderSize(W, H)  # Alternative to setPixelScale
    d.saveSvg('out/{}.svg'.format(name))
    # d.savePng('out/{}.png'.format(name))



def draw_grid(svg_elem, out_file, order_n):

    d = draw.Drawing(W, H, origin='center', displayInline=False)
    elem = Element(svg_elem)
    d.append(draw.Rectangle(-W / 2, -W / 2, W, H, fill='#A9BBC6'))

    for x in range(-3, 4):
        for y in range(-3, 4):
            draw_n_ord(order_n, elem, d, (x+3)*5.5, (y-3)*5.5, x*100*1.1, y*100*1.1)

    d.setRenderSize(W, H)
    d.saveSvg(out_file + '.svg')
    d.savePng(out_file + '.png')


if __name__ == '__main__':
    ch = 'R'
    order_n = 5
    svg_elem = draw.Text('R', 60, 0, 0)
    out_dir = 'out'
    out_file = '{}_{}'.format(ch, str(order_n))
    draw_grid(svg_elem, os.path.join(out_dir, out_file), order_n)

    im = Image.open(os.path.join(out_dir, out_file) + '.png')
    im.show()
