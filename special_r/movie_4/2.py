import os

import drawSvg as draw
from special_r.svg.Transformation import *
from special_r.svg.shapes import *
from special_r.svg.Transformation import *
from special_r.svg.Element import Element, Motif


f_svg = draw.Text('G', 100 , 0, 0)


def main(out_dir='out/2/1'):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    x_p, y_p = 0, 0
    single_line = True
    diagonal = False


    iters = 1000
    elem = Element(f_svg)
    translations = []
    rotations = []
    elements = []


    if single_line:
        for x in range(-4, 4):
            for y in range(1):
                elements.append(Translation(x*200, -y*100)(elem))
                rotations.append(Rotation(360./iters, (x*200) +(x*20), -((y*100)+ (y*20))))
    if diagonal:
        for x in range(-4, 4):
            for y in range(-4, 4):
                if x==y or x ==-y:
                    elements.append(Translation(x*200, -y*100)(elem))
                    rotations.append(Rotation(360./iters, (x*200) +(x*20), -((y*100)+ (y*20))))




    for i in range(iters):
        print(i)
        sur = draw.Drawing(1920, 1080, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-1920/2, -1080/2, 1920, 1080, fill='#A9BBC6'))

        for j in range(len(elements)):
            rot = rotations[j]
            elements[j] = rot(elements[j])
            elements[j].draw(sur)
            sur.append(draw.Circle(rot.x, -rot.y, 5, fill="#8C0303"))


        #sur.saveSvg('out/1/{}.svg'.format(str(i)))

        #sur.setRenderSize(1800, 1800)  # Alternative to setPixelScale
        sur.savePng(os.path.join(out_dir,'{}.png'.format(str(i).zfill(4))))



if __name__ == '__main__':
    main()