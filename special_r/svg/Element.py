import copy

import drawSvg as draw

from special_r.svg.Transformation import *
from special_r.svg.shapes import *


class Element(object):
    def __new__(cls, *args, **kwargs):

        instance = super(Element, cls).__new__(cls)
        instance.id = hash(instance)
        return instance

    def __init__(self, svg_elem):
        self.svg_elem = svg_elem
        self.rotation = (0, 0, 0)
        self.translation = (0, 0)
        self.transform = ''
        self.id = str(hash(self))



    def draw(self, surface):
        self.svg_elem.args['transform'] = self.transform
        self.svg_elem.id = self.id
        surface.append(self.svg_elem)

    def apply_transform(self, transform_str):
        self.transform =   transform_str + self.transform


class Motif:

    def __init__(self, element, transforms):

        self.elements = [t(element) for t in transforms]

    def apply_transform(self, transform_str):
        for e in self.elements:
            e.apply_transform(transform_str)

    def draw(self, surface):
        for e in self.elements:
            e.draw(surface)




if __name__ == '__main__':
    name = 'blob128'

    d = draw.Drawing(900, 900, origin='center', displayInline=False)
    rotations = [TransChain([Rotation(i*45, 0, 0), Translation(20,10)]) for i in range(0,8)]
    elem = Element(t_svg)
    motif = Motif(elem, rotations)
    translations = [Translation(x*200, y*200) for x in range(-5,5) for y in range(-5, 5)]
    motif2 = Motif(motif, translations)
    motif.apply_transform('translate(10, 10)')
    motif2.draw(d)
    d.setRenderSize(1800, 1800)  # Alternative to setPixelScale
    d.saveSvg('{}.svg'.format(name))
    # d.savePng('out/{}.png'.format(name))
