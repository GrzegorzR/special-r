import copy


class Transformation:

    def __init__(self, trans_str):
        self.trans_str = trans_str

    def __call__(self, *args, **kwargs):
        elem = args[0]
        res = copy.deepcopy(elem)
        res.apply_transform(self.trans_str)
        return res





class Rotation(Transformation):
    def __init__(self, r, x, y):
        self.r, self.x, self.y = r, x, y
        trans_str = 'rotate({}, {}, {}) '.format(str(self.r), str(self.x), str(self.y))
        super().__init__(trans_str)



class Translation(Transformation):
    def __init__(self, x, y):
        self.x, self.y =x, y
        trans_str = 'translate({}, {}) '.format(str(self.x), str(self.y))
        super().__init__(trans_str)


class TransChain(Transformation):
    def __init__(self, transforms):
        trans_str = ''.join([t.trans_str for t in transforms])

        super().__init__(trans_str)


