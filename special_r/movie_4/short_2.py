import copy
import os
import random
from planar import Vec2, Affine
import drawSvg as draw
import numpy as np

from special_r.svg.Transformation import *
from special_r.svg.shapes import *
from special_r.svg.Transformation import *
from special_r.svg.Element import Element, Motif


t_svg = draw.Text('t', 80 , 0, 0, fill=None)


#W, H = 1920, 1080
W, H = 1080/2, 1920/2
main_iterator = 0


def rotate(p, origin=(0, 0), degrees=0):
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    res = np.squeeze((R @ (p.T-o.T) + o.T).T)
    dif = p - res
    return np.around(np.array([res[0], p[0][1]-dif[0][1]]),0)


class ElementDoubleRotation:

    def __init__(self,  svg_elem, r_p1, r_p2, draw_rot_points=True):
        self.svg_elem = svg_elem
        #self.center = np.array(center)
        self.r_p1 = Vec2(r_p1[0], r_p1[1])
        self.r_p2 = Vec2(r_p2[0], r_p2[1])
        self.transform_mat = Affine.identity()
        self.draw_rot_points = draw_rot_points


    def rot(self, a, rot_p):
        res = copy.copy(self)
        #rot1 = Affine.rotation(100, (0,-100))
        #
        rot =Affine.rotation(a, rot_p)

        res.transform_mat = res.transform_mat * rot
        res.r_p1 = rot * res.r_p1
        res.r_p2 = rot * res.r_p2
        return res

    def rot1(self, a):
        return self.rot(a, self.r_p1)

    def rot2(self, a):
        return self.rot(a, self.r_p2)

    #def rot1(self,a):
    #    res = copy.deepcopy(self)
    #    t = Rotation(a,  self.r_p1[0], self.r_p1[1])
    #    res.apply_transform(t.trans_str)
    #    res.r_p2 = rotate(res.r_p2, res.r_p1, a)
    #    #res.r_p2[0] += random.random()*10
    #    return res
#
    #def rot2(self, a):
    #    res = copy.deepcopy(self)
    #    t = Rotation(a, self.r_p2[0], self.r_p2[1])
    #    res.apply_transform(t.trans_str)
    #    res.r_p1 = rotate(res.r_p1, res.r_p2, a)
    #    return res

    #def rot1(self, a):
    #    return self.rotate(a ,)
    #def rot2(self, a):
    #    return self.rotate(a , self.r_p2[0], self.r_p2[1])


    def draw(self, surface):
        columns = self.transform_mat.column_vectors
        #tmp_str = ' '.join(tmp_str)
        transform = 'matrix({} {} {} {} {} {}) '.format(columns[0][0], columns[0][1],
                                                        columns[1][0], columns[1][1],
                                                        columns[2][0], -columns[2][1])

        elem = draw.Text('t', 80 , 0, 0, fill=None)
        elem.args['transform'] = transform
        surface.append(elem)
        if self.draw_rot_points:

            surface.append(draw.Circle(int(self.r_p1[0]), int(self.r_p1[1]), 5, fill="red"))
            surface.append(draw.Circle(int(self.r_p2[0]), int(self.r_p2[1]), 5, fill="blue"))

def main(input_svg):
    sur = draw.Drawing(W, H, origin='center', displayInline=False)

    sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))

    e = ElementDoubleRotation(input_svg, [0, 50], [50, 0], draw_rot_points=True)
    e.draw(sur)
    ord_num = 3
    new_arr = []
    for i in range(ord_num):
        #print(e.transform_mat)
        e_tmp = e.rot1(np.around((360. / ord_num) * i, 0))
        #print(e_tmp.transform_mat)
        e_tmp.draw(sur)
        print(e_tmp.r_p2)
        new_arr.append(e_tmp)
    #sur.append(draw.Circle(50, 50, 5, fill="green"))
    new_arr2 = []
    for j,e in enumerate(new_arr):
        print(j)
        for i in range(ord_num):
            e_tmp = e.rot2(np.around((360. / ord_num) * i,0))
            #e_tmp.draw(sur)
            new_arr2.append(e_tmp)
    print(len(new_arr2))
    for j,e in enumerate(new_arr2):
        print(j)
        for i in range(ord_num):
            e_tmp = e.rot1(np.around((360. / ord_num) * i,0))
            #e_tmp.draw(sur)


    sur.savePng('out/tes4.png')
    sur.saveSvg('out/tes4.svg')
    #sur.saveSvg('test12aa.svg')

def animate_order(input_element, i, iters_num, order_n, rot_type, sur):

    angle = (360./iters_num)*i

    for n in range(1,order_n-1):
        #print(i/iters_num, n/order_n, i/iters_num >= n/order_n)
        if i/iters_num >= n/order_n:
            if rot_type == 1:
                e = input_element.rot1((n/order_n)*360.)
            else :
                e = input_element.rot2((n/order_n)*360.)
            e.draw(sur)

    if rot_type == 1:
        e = input_element.rot1(angle)
    else:
        e = input_element.rot2(angle)
    e.draw(sur)

pos_set = set()

def animation_t(input_svg, out_dir):
    os.makedirs(out_dir, exist_ok=True)


    iters = 24

    e = ElementDoubleRotation(input_svg, [-40, -40], [40, 50], draw_rot_points=True)
    ord_num = 3

    def animate_list(elements_list, iters, rot_type, out_dir, sur):
        global main_iterator

        for i in range(iters + 1):
            print(main_iterator, len(elements_list))
            main_iterator +=1
            sur_tmp = copy.deepcopy(sur)
            for e in elements_list:
                animate_order(e, i, iters, ord_num, rot_type, sur_tmp)
                sur_tmp.savePng(os.path.join(out_dir, '{}.png'.format(str(main_iterator).zfill(4))))
                #sur_tmp.saveSvg(os.path.join(out_dir, '{}.svg'.format(str(main_iterator).zfill(4))))

        new_arr = []
        for e in elements_list:
            for i in range(1,ord_num):
                if rot_type ==1:
                    e_tmp = e.rot1(np.around((360. / ord_num) * i, 0))

                else:
                    e_tmp = e.rot2(np.around((360. / ord_num) * i, 0))
                t = tuple(np.round(tuple(e_tmp.transform_mat), 2))
                if t not in pos_set:
                    pos_set.add(t)
                    new_arr.append(e_tmp)
        return new_arr, sur_tmp

    sur = draw.Drawing(W, H, origin='center', displayInline=False)
    sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))

    new_arr, sur = animate_list([e], iters, 1, out_dir, sur)
    new_arr, sur = animate_list(new_arr +[e], iters, 2, out_dir, sur)
    new_arr, sur = animate_list(new_arr, iters, 1, out_dir, sur)
    new_arr, sur = animate_list(new_arr, iters, 2, out_dir, sur)
    new_arr, sur = animate_list(new_arr, iters, 1, out_dir, sur)
    new_arr, sur = animate_list(new_arr, iters, 2, out_dir, sur)
    new_arr, sur = animate_list(new_arr, iters, 1, out_dir, sur)
    new_arr, sur = animate_list(new_arr, iters, 2, out_dir, sur)
    #for i in range(ord_num):
    #    e_tmp = e.rot1((360. / ord_num) * i)
    #    new_arr.append(e_tmp)
#
    #for i in range(iters+1):
    #    print(i)
    #    sur = draw.Drawing(W, H, origin='center', displayInline=False)
    #    sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))
    #    for e in new_arr:
    #        animate_order(e, i, iters, ord_num, 2, sur)
    #        sur.savePng(os.path.join(out_dir, '{}.png'.format(str(i).zfill(4))))
#
if __name__ == '__main__':
    out_dir = 'out/short_2/test1'


    #main(t_svg)
    animation_t(t_svg, 'out/short_2/video2')
    #
    #animation_t(blob_svg, 'out/short_2/video3')
    #animation_t(line2_svg, 'out/short_2/video4')
    #animation_t(line3_svg, 'out/short_2/video5')
    #animation_t(strange_triangular_svg, 'out/short_2/video6')
