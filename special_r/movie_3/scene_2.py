import drawSvg as draw
from special_r.svg.Transformation import *
from special_r.svg.shapes import *
from special_r.svg.Transformation import *
from special_r.svg.Element import Element, Motif



f_svg =  draw.Text('G', 50 , 0, 0)

def draw_n_ord(n, element, sur, x_p, y_p, x_t, y_t):
        rotations = [TransChain([Rotation(i * (360/n) , x_p, y_p)]) for i in range(0, n)]
        motif = Motif(element, rotations)
        motif = Translation(-x_p, -y_p)(motif)
        motif = Translation(x_t, y_t)(motif)
        motif.draw(sur)

def order_3():
    name = 'order_3'


    d = draw.Drawing(900, 900, origin='center', displayInline=False)
    elem = Element(f_svg)
    for x in range(-10, 10):
        for y in range(-10, 10):
            draw_n_ord(5, elem, d,(x+2)*4, (y-3)*5, x*100, y*100)


    d.setRenderSize(1800, 1800)  # Alternative to setPixelScale
    d.saveSvg('out/{}.svg'.format(name))
    # d.savePng('out/{}.png'.format(name))

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




    d.setRenderSize(1800, 1800)  # Alternative to setPixelScale
    d.saveSvg('out/{}.svg'.format(name))
    # d.savePng('out/{}.png'.format(name))


if __name__ == '__main__':
    order_3()
    #order_2()
