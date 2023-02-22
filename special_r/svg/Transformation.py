import copy

from special_r.svg.Element import ElementContainer


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
        self.x, self.y = x, y
        trans_str = 'translate({}, {}) '.format(str(self.x), str(self.y))
        super().__init__(trans_str)


class Glide(Transformation):
    def __init__(self):
        trans_str = 'matrix(-1 0 0 -1 0 0) '
        super().__init__(trans_str)


class ReflectX(Transformation):
    def __init__(self):
        trans_str = 'matrix(-1 0 0 1 0 0) '
        super().__init__(trans_str)

class Scale(Transformation):
    def __init__(self, scale_parameter):
        trans_str = 'scale({}) '.format(scale_parameter)
        super().__init__(trans_str)

class CustomTransformation(Transformation):
    def __init__(self, t_mat):
        trans_str = 'matrix({} {} {} {} {} {}) '.format(t_mat[0][0], t_mat[1][0], t_mat[0][1],
                                                        t_mat[1][1], t_mat[0][1], t_mat[1][2])
        super().__init__(trans_str)


class TransChain(Transformation):
    def __init__(self, transforms):
        trans_str = ''.join([t.trans_str for t in transforms])

        super().__init__(trans_str)

class RoseTrans():

    def __init__(self, order_num, x_p=0, y_p=0):
        self.order_num = order_num
        self.x_p = x_p
        self.y_p = y_p

    def __call__(self, *args, **kwargs):
        elem = args[0]
        elem_copy = copy.deepcopy(elem)
        result = []
        for n in range(self.order_num):
             result.append(Rotation((n / self.order_num) * 360., self.x_p, self.y_p)(elem_copy))

        return ElementContainer(result)
