import drawSvg as draw
from special_r.svg.Transformation import *
from special_r.svg.shapes import *
from special_r.svg.Transformation import *
from special_r.svg.Element import Element, Motif


f_svg = draw.Text('G', 100 , 0, 0)


def main():
    x_p, y_p = 0, 0

    iters = 1000
    elem = Element(f_svg)


    rot = Rotation(360./iters, x_p, y_p)
    for i in range(iters):
        print(i)
        sur = draw.Drawing(1920, 1080, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-1920/2, -1080/2, 1920, 1080, fill='#A9BBC6'))
        sur.append(draw.Circle(x_p, y_p, 5, fill="#8C0303"))

        elem = rot(elem)
        elem.draw(sur)

        #sur.saveSvg('out/1/{}.svg'.format(str(i)))
        sur.savePng('out/1/{}.png'.format(str(i).zfill(4)))



if __name__ == '__main__':
    main()