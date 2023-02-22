import os
import drawSvg as draw
import numpy as np

from special_r.svg.Transformation import *
from special_r.svg.shapes import *
from special_r.svg.Transformation import *
from special_r.svg.Element import Element, Motif


f_svg = draw.Text('G', 250 , 0, 0)


W, H = 1920*2, 1080*2
#W, H = 1080, 1920

def main(out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    x_p, y_p = 0, 0

    iters = 240*4
    elem = Element(f_svg)


    rot = Rotation(360./iters, x_p, y_p)
    for i in range(iters):
        print(i)
        sur = draw.Drawing(W, H, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-W/2, -H/2, W, H, fill='#A9BBC6'))
        sur.append(draw.Circle(x_p, y_p, 5, fill="#8C0303"))

        elem = rot(elem)
        elem.draw(sur)

        #sur.saveSvg('out/1/{}.svg'.format(str(i)))
        sur.savePng(os.path.join(out_dir,'{}.png'.format(str(i).zfill(4))))



if __name__ == '__main__':
    #out_dir = 'out/1/vertical'
    #main(out_dir)

    out_dir = 'out/1/1'
    main(out_dir)
    #iscene_vertical_out(out_dir, iters)