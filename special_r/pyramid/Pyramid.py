import itertools

import numpy as np
import pygame
import math
from math import sin, cos

from colour import Color

from special_r.BasicRect import BasicRect
from special_r.BorderRect import BorderRect
from special_r.Scene import Scene
from special_r.utils.parametric_functions import create_transition_fun, create_linear_transition_fun


class Pyramid:
    def __init__(self, x, y, w, h, colors, scale=0.9, x_t=0., y_t=0., height=5, border=2., vr=0.0, borders_colors=None):
        # x,y,w,h - position and size of the base rect in pyramid
        # scale - (0,1) size of the each next rect
        #
        # x_t, y_t [-1, 1] - position of the center next rect where 0 - the same position,
        # 1, -1 - edge of the lower rect
        #
        # height - number of layers in the pyramid

        self.x, self.y = x, y
        self.w, self.h = w, h
        self.x_t, self.y_t = x_t, y_t
        self.scale = scale
        self.height = height
        self.vr = vr
        self.border = border
        self.colors = colors
        self.rects = []
        if borders_colors is None:
            self.borders_colors = ['#000000' for _ in range(height)]
        else:
            self.borders_colors = borders_colors
        self.updates_rects()

    def updates_rects(self):
        scale_v = 1
        s_x, s_y = 0., 0.

        for n in range(self.height):
            x = self.x + self.w * s_x
            y = self.y + self.w * s_y
            # self.rects.append(BasicRect(x, y, self.w*scale_v, self.h*scale_v, color=c[n]))
            self.rects.append(BorderRect(x, y, self.w * scale_v, self.h * scale_v, border=self.border, vr=self.vr,
                                         color=self.colors[n % len(self.colors)],
                                         border_color=self.borders_colors[n % len(self.borders_colors)]))
            scale_v *= self.scale
            s_x += scale_v * self.x_t
            s_y += scale_v * self.y_t

    def update(self, ts):
        for r in self.rects:
            r.update(ts)

    def draw(self, surface):
        for r in self.rects:
            r.draw(surface)


class PyramidMoving(Pyramid):

    def __init__(self, x, y, w, h, xyt_fun, colors, scale=0.99,
                 height=20, anim_param=1., vr=0.0, border=2., borders_colors=None):
        super().__init__(x, y, w, h, scale=scale, height=height, colors=colors,
                         vr=vr, border=border, borders_colors=borders_colors)
        self.t = 0.
        self.animation_parameter = anim_param


        self.xyt_fun = xyt_fun
        self.x_t, self.y_t = self.xyt_fun(self.t)
        self.x_t, self.y_t = self.x_t / self.animation_parameter, self.y_t / self.animation_parameter

        self.size_fun = lambda t: (w, h)
        self.height_fun = lambda t: height
        self.scale_fun = lambda t: scale
        self.pos_fun = lambda t: (x, y)
        self.color_fun = lambda t: colors
        self.borders_colors_fun = lambda t: self.borders_colors

    def change_xyt(self, x1, y1, translation_time=10.):
        x0, y0 = self.x_t, self.y_t
        t0, t1 = self.t, self.t + translation_time

        transition_fun_x = create_transition_fun(x0, x1, t0, t1,3)
        transition_fun_y = create_transition_fun(y0, y1, t0, t1,3)
        self.xyt_fun = lambda t: (transition_fun_x(t), transition_fun_y(t))

    def change_xt(self, x1, translation_time=10.):
        self.change_xyt(x1, self.y_t, translation_time)

    def change_yt(self, y1, translation_time=10.):
        self.change_xyt(self.x_t, y1, translation_time)

    def change_height(self, h1, translation_time=15):
        h0 = self.height
        t0, t1 = self.t, self.t + translation_time

        transition_fun_h = create_transition_fun(h0, h1, t0, t1)
        self.height_fun = lambda t: round(transition_fun_h(t))

    def change_scale(self, s1, translation_time=10):
        s0 = self.scale
        t0, t1 = self.t, self.t + translation_time

        transition_fun_h = create_transition_fun(s0, s1, t0, t1)
        self.scale_fun = lambda t: transition_fun_h(t)

    def change_size(self, h1, w1, translation_time):
        h0, w0 = self.h, self.w
        t0, t1 = self.t, self.t + translation_time

        transition_fun_h = create_transition_fun(h0, h1, t0, t1)
        transition_fun_w = create_transition_fun(w0, w1, t0, t1)
        self.size_fun = lambda t: (transition_fun_w(t), transition_fun_h(t))

    def change_h(self, h1, translation_time):
        self.change_size(h1, self.w, translation_time)

    def change_w(self, w1, translation_time):
        self.change_size(self.h, w1, translation_time)

    def change_pos(self, x1, y1, translation_time):
        x0, y0 = self.x, self.y
        t0, t1 = self.t, self.t + translation_time
        transition_fun_x = create_transition_fun(x0, x1, t0, t1)
        transition_fun_y = create_transition_fun(y0, y1, t0, t1)
        self.pos_fun = lambda t: (int(transition_fun_x(t)), int(transition_fun_y(t)))

    def change_colorset(self, new_colorset, transition_time=10.):
        old_colorset = self.colors
        t0, t1 = self.t, self.t + transition_time
        v0, v1 = 0, max(len(new_colorset), len(old_colorset)) + 1

        t_fun = create_linear_transition_fun(v0, v1, t0, t1)
        t_fun_round = lambda t: round(t_fun(t))
        self.color_fun = lambda t:  new_colorset[:t_fun_round(t)] + old_colorset[t_fun_round(t):]

    def change_colorset_linear(self, new_colorset, transition_time=10.):
        old_colorset = self.colors
        t0, t1 = self.t, self.t + transition_time

        new_colorset= itertools.cycle(new_colorset)
        new_colorset_equal = []
        


        transition_fun = create_transition_fun(0, 1., t0, t1)
        def linear_color_fun(t):
            new_colors = []
            for i, c in enumerate(old_colorset):
                c0 = np.array(Color(c).rgb)
                c1 = np.array(Color(next(new_colorset)).rgb)
                t_val = transition_fun(t)
                new_color = Color(rgb=c0*t_val + c1*(1.-t_val))
                #print(type(new_color))
                new_colors.append(new_color.hex_l.upper())
            return new_colors

        self.color_fun = lambda t: linear_color_fun(t)

    def change_borders_colorstes(self, new_colorset, transition_time=10.):
        old_colorset = self.borders_colors
        t0, t1 = self.t, self.t + transition_time

        v0, v1 = 0, max(len(new_colorset), len(old_colorset)) + 1

        t_fun = create_linear_transition_fun(v0, v1, t0, t1)
        t_fun_round = lambda t: round(t_fun(t))
        self.borders_colors_fun = lambda t:  new_colorset[:t_fun_round(t)] + old_colorset[t_fun_round(t):]

    def update(self, ts):
        self.rects = []
        self.height = self.height_fun(self.t)
        self.scale = self.scale_fun(self.t)
        self.w, self.h = self.size_fun(self.t)
        self.x_t, self.y_t = self.xyt_fun(self.t)
        self.x_t, self.y_t = self.x_t / self.animation_parameter, self.y_t / self.animation_parameter
        self.x, self.y = self.pos_fun(self.t)
        self.colors = self.color_fun(self.t)
        self.borders_colors = self.borders_colors_fun(self.t)
        self.updates_rects()
        super(PyramidMoving, self).update(ts)
        self.t += ts


def simple():
    x, y = 401, 401.
    w, h = 401., 201.

    p = Pyramid(x, y, w, h, scale=0.8, x_t=0.1, y_t=0.04, height=8)
    p2 = Pyramid(200., 200., 100., 200., scale=0.5, x_t=0.4, height=3)
    s = Scene([p, p2])
    s.animate(0)


def simple2():
    x, y = 401, 401.
    w, h = 401., 201.
    p = PyramidMoving(x, y, w, h, scale=0.96, x_t=0., y_t=0.0, height=20)
    p2 = PyramidMoving(x, 300, w, h, scale=0.92, x_t=0., y_t=0.0, height=20)
    s = Scene([p, p2])
    s.animate(0)


if __name__ == '__main__':
    # simple()
    simple2()
