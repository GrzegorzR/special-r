
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
        self.transform = transform_str + self.transform


class ElementContainer:
    def __init__(self, elements):
        self.elements = elements

    def apply_transform(self, transform_str):
        for e in self.elements:
            e.apply_transform(transform_str)

    def draw(self, surface):
        for e in self.elements:
            e.draw(surface)


class Motif(ElementContainer):
    def __init__(self, element, transforms):
        elements = [t(element) for t in transforms]
        super().__init__(elements)


