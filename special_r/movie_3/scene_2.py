import drawSvg as draw
from special_r.svg.Transformation import *
from special_r.svg.shapes import *
from special_r.svg.Transformation import *
from special_r.svg.Element import Element, Motif



f_svg =  draw.Text('f', 110 , 0, 0)


def order_3():
    name = 'order_3'

    d = draw.Drawing(900, 900, origin='center', displayInline=False)
    rotations = [TransChain([Rotation(i * 120 , 40, -30)]) for i in range(0, 3)]
    elem = Element(f_svg)
    motif = Motif(elem, rotations)


    motif.draw(d)
    d.setRenderSize(1800, 1800)  # Alternative to setPixelScale
    d.saveSvg('out/{}.svg'.format(name))
    # d.savePng('out/{}.png'.format(name))

def order_2():
    name = 'order_2_2'

    d = draw.Drawing(900, 900, origin='center', displayInline=False)
    rotations = [TransChain([Rotation(i * 180 , 17, -10)]) for i in range(0, 2)]
    elem = Element(f_svg)
    motif = Motif(elem, rotations)


    motif.draw(d)
    d.setRenderSize(1800, 1800)  # Alternative to setPixelScale
    d.saveSvg('out/{}.svg'.format(name))
    # d.savePng('out/{}.png'.format(name))


if __name__ == '__main__':
    order_3()
    order_2()
