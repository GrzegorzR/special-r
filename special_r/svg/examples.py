import os
import drawSvg as draw

from special_r.svg.Element import Element, Motif
from special_r.svg.Transformation import Translation, Rotation


W,H = 1920, 1080

def rosseta(out_dir, input_svg):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    elem = Element(input_svg)
    elem_1 = Translation(-60, -160)(elem)
    elem_1 = Rotation(20,0,-140)(elem)

    elem_2 = Translation(-20, -25)(elem)
    elem_2 = Rotation(20,0,-150)(elem_2)

    elem_3 = Translation(-70, -10)(elem)

    ord_num =36

    transforms = [Rotation(360/ord_num*i, 0,0) for i in range(ord_num)]
    m = Motif(elem_1, transforms)
    m2 = Motif(elem_2, transforms)
    #m3 = Motif(elem_3, transforms)

    sur = draw.Drawing(W, H, origin='center', displayInline=False)

    sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))
    #draw_order(sur, m, 3,360, 0,0, 100,100)
    m.draw(sur)
    m2.draw(sur)
    #m3.draw(sur)
    sur.savePng('test12aa.png')
    sur.saveSvg('test12aa.svg')