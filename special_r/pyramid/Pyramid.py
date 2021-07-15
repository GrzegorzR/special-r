import numpy as np
import pygame
from math import sin, cos

from special_r.BasicRect import BasicRect
from special_r.BorderRect import BorderRect
from special_r.Scene import Scene


class Pyramid:
    def __init__(self, x, y, w, h, colors, scale=0.9, x_t=0., y_t=0., height=5, border=0., vr=0.0):
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
        self.border= border
        self.colors = colors
        self.rects = []
        self.updates_rects()

    def updates_rects(self):
        scale_v = 1
        s_x, s_y = 0., 0.

        for n in range(self.height):
            x = self.x + self.w * s_x
            y = self.y + self.w * s_y
            # self.rects.append(BasicRect(x, y, self.w*scale_v, self.h*scale_v, color=c[n]))
            self.rects.append(BorderRect(x, y, self.w * scale_v, self.h * scale_v, border=self.border, vr=self.vr,
                                         color=self.colors[n % len(self.colors)]))
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

    def __init__(self, x, y, w, h, move_fun, colors, scale=0.99, height=20, vr=0.0):
        super().__init__(x, y, w, h, scale=scale, height=height, colors=colors, vr=vr)
        self.t = 0.
        self.animation_parameter = 10.
        self.move_fun = move_fun
        self.x_t, self.y_t = self.move_fun(self.t)
        self.x_t, self.y_t = self.x_t / self.animation_parameter, self.y_t / self.animation_parameter

    def update(self, ts):
        self.t += ts
        print(self.t)
        self.rects = []
        self.x_t, self.y_t = self.move_fun(self.t)
        #print(self.x_t, self.y_t)
        self.x_t, self.y_t = self.x_t / self.animation_parameter, self.y_t / self.animation_parameter
        self.updates_rects()
        super(PyramidMoving, self).update(ts)


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
    p2 = PyramidMoving(300, 300, w, h, scale=0.92, x_t=0., y_t=0.0, height=20)
    s = Scene([p, p2])
    s.animate(0)


if __name__ == '__main__':
    # simple()
    simple2()
