#!/usr/bin/env python

import math
import cairo
import os
import numpy as np
from math import pi, sin, cos
from special_r.svg.Transformation import *

W, H = 1080, 1920
BG_COL = (169 / 255, 187 / 255, 198 / 255)
main_iterator = 0
pos_set = set()


def scale_fun(iteration, iter_max=1000, s_max=3.):
    if iteration >= iter_max:
        return 1.
    else:
        return -(iteration / iter_max) * (s_max - 1) + s_max

def draw_R_fun(ctx):
    ctx.set_source_rgba(0.2, 0.2, 0.55,0.1)
    ctx.select_font_face("Courier", cairo.FONT_SLANT_NORMAL)
    ctx.set_font_size(100)
    ctx.show_text("R")
    ctx.set_line_width(10)
    ctx.stroke()


class ElementDoubleRotation:

    def __init__(self, center, r_p1, r_p2, draw_rot_points=True, draw_obj_fun=draw_R_fun):
        self.center = center

        # self.center = np.array(center)
        self.transform_mat = cairo.Matrix()
        self.transform_mat.translate(center[0], center[1])
        self.r_p1 = r_p1
        self.r_p2 = r_p2

        self.draw_obj_fun = draw_obj_fun

        self.draw_rot_points = draw_rot_points

    def rot(self, a, rot_p):
        res = copy.copy(self)
        res.transform_mat = self.transform_mat.multiply(cairo.Matrix())
        res.transform_mat.translate(rot_p[0], rot_p[1])
        res.transform_mat.rotate(a)
        res.transform_mat.translate(-rot_p[0], -rot_p[1])
        return res

    def rot1(self, a):
        return self.rot(a, self.r_p1)

    def rot2(self, a):
        return self.rot(a, self.r_p2)

    def draw(self, ctx):
        ctx.save()
        ctx.transform(self.transform_mat)

        self.draw_obj_fun(ctx)


        if self.draw_rot_points:
            # p1 = self.transform_mat.transform_point(0,0)

            ctx.arc(self.r_p1[0], self.r_p1[1], 5, 0, 2 * math.pi)
            ctx.set_source_rgb(0, 0, 0.6)
            ctx.fill()
            ctx.arc(self.r_p2[0], self.r_p2[1], 5, 0, 2 * math.pi)
            ctx.set_source_rgb(0.6, 0, 0.)

        ctx.fill()
        ctx.restore()


def animate_order(input_element, i, iters_num, order_n, rot_type, sur):
    angle = (2 * math.pi / iters_num) * i

    for n in range(0, order_n):
        # print(i/iters_num, n/order_n, i/iters_num >= n/order_n)
        if i / iters_num >= n / order_n:
            if rot_type == 1:
                e = input_element.rot1((n / order_n) * 2 * math.pi)
            else:
                e = input_element.rot2((n / order_n) * 2 * math.pi)
            e.draw(sur)

    if rot_type == 1:
        e = input_element.rot1(angle)
    else:
        e = input_element.rot2(angle)
    e.draw(sur)


def animation_t(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, int(W), int(H))
    ctx = cairo.Context(surface)

    iters = 120
    x1_p, y1_p = 50, -70
    x2_p, y2_p = 0, 50

    e = ElementDoubleRotation((W / 2, H / 2), [x1_p, y1_p], [x2_p, y2_p], draw_rot_points=True)
    ord_num = 3

    def animate_list(elements_list, old_list, iters, rot_type, out_dir, ctx, draw=True):
        global main_iterator

        for i in range(iters):
            print(main_iterator, len(elements_list))
            main_iterator += 1
            ctx.set_source_rgb(*BG_COL)
            ctx.rectangle(0, 0, W * 1.5, H * 1.5)
            ctx.fill()
            ctx.save()

            s = scale_fun(main_iterator, iters * 5, 3.)

            ctx.translate(((W / 2) - ((W / 2) * s)), ((H / 2) - ((H / 2) * s)))
            # print()
            ctx.scale(s, s)
            ctx.translate(-x1_p, -y1_p)
            for e in old_list:
                e.draw(ctx)
            for e in elements_list:
                if draw:
                    animate_order(e, i, iters, ord_num, rot_type, ctx)
                    surface.write_to_png(os.path.join(out_dir, '{}.png'.format(str(main_iterator).zfill(4))))
                # sur_tmp.saveSg(os.path.join(out_dir, '{}.svg'.format(str(main_iterator).zfill(4))))
            ctx.restore()
        new_arr = []
        for e in elements_list:
            for i in range(1, ord_num):
                if rot_type == 1:
                    e_tmp = e.rot1(((2 * math.pi) / ord_num) * i)
                    t = tuple(np.round(tuple(e_tmp.transform_mat), 2))
                    if t not in pos_set:
                        pos_set.add(t)
                        new_arr.append(e_tmp)
                else:
                    e_tmp = e.rot2(((2 * math.pi) / ord_num) * i)
                    t = tuple(np.round(tuple(e_tmp.transform_mat), 2))
                    if t not in pos_set:
                        pos_set.add(t)
                        new_arr.append(e_tmp)

        print(pos_set)
        return new_arr, old_list + elements_list

    new_arr, old_arr = [e], []
    new_arr, old_arr = animate_list(new_arr, [], iters, 1, out_dir, ctx)
    new_arr, old_arr = animate_list(new_arr + [e], old_arr, iters, 2, out_dir, ctx)
    new_arr, old_arr = animate_list(new_arr, old_arr, iters, 1, out_dir, ctx)
    new_arr, old_arr = animate_list(new_arr, old_arr, iters, 2, out_dir, ctx)
    new_arr, old_arr = animate_list(new_arr, old_arr, iters, 1, out_dir, ctx)
    new_arr, old_arr = animate_list(new_arr, old_arr, iters, 2, out_dir, ctx)
    new_arr, old_arr = animate_list(new_arr, old_arr, iters, 1, out_dir, ctx)
    new_arr, old_arr = animate_list(new_arr, old_arr, iters, 2, out_dir, ctx)
    new_arr, old_arr = animate_list(new_arr, old_arr, iters, 1, out_dir, ctx)
    new_arr, old_arr = animate_list(new_arr, old_arr, iters, 2, out_dir, ctx)
    new_arr, old_arr = animate_list(new_arr, old_arr, iters, 1, out_dir, ctx)
    new_arr, old_arr = animate_list(new_arr, old_arr, iters, 2, out_dir, ctx)
    new_arr, old_arr = animate_list(new_arr, old_arr, iters, 1, out_dir, ctx)


def change_rotations_points(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, int(W), int(H))
    ctx = cairo.Context(surface)

    def generate_single_img(x1_p, y1_p, x2_p, y2_p, out_file, ctx):
        ctx.set_source_rgb(*BG_COL)
        ctx.rectangle(0, 0, W * 1.5, H * 1.5)
        ctx.fill()

        ctx.save()
        ctx.translate(-x1_p, -y1_p)
        # x1_p, y1_p = 50, -70
        # x2_p, y2_p = 0, 50

        e = ElementDoubleRotation((W / 2, H / 2), [x1_p, y1_p], [x2_p, y2_p], draw_rot_points=True)
        ord_num = 7
        pos_set = set()

        def get_elements_list(elements_list, old_list, rot_type):
            for e in elements_list:
                for i in range(1, ord_num):
                    if rot_type == 1:
                        e_tmp = e.rot1(((2 * math.pi) / ord_num) * i)
                        t = tuple(np.round(tuple(e_tmp.transform_mat), 2))
                        if t not in pos_set:
                            pos_set.add(t)
                            new_arr.append(e_tmp)
                    else:
                        e_tmp = e.rot2(((2 * math.pi) / ord_num) * i)
                        t = tuple(np.round(tuple(e_tmp.transform_mat), 2))
                        if t not in pos_set:
                            pos_set.add(t)
                            new_arr.append(e_tmp)
            return new_arr, old_list + elements_list

        new_arr, old_arr = [e], []
        new_arr, old_arr = get_elements_list(new_arr, [], 1)
        new_arr, old_arr = get_elements_list(
            new_arr + [e], old_arr, 2)
        for i in range(2):
            new_arr, old_arr = get_elements_list(new_arr, old_arr, (i % 2) + 1)

        all = new_arr + old_arr
        for e in all:
            e.draw(ctx)

        surface.write_to_png(out_file)
        ctx.restore()

    for i in range(240 * 8):
        print(i)
        img_path = os.path.join(out_dir, '{}.png'.format(str(i).zfill(4)))
        x1_p, y1_p = sin((i * (pi / 240)) + pi / 2) * 50., -70
        x2_p, y2_p = 0, sin((i * (pi / 240)) + pi / 2) * 50.
        generate_single_img(x1_p, y1_p, x2_p, y2_p, img_path, ctx)


if __name__ == '__main__':
    # animation_t('out/short_2/video9')

    change_rotations_points('out/short_2/change_rot_point4')
