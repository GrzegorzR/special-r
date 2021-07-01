import numpy as np
import pygame

from special_r.BasicRect import BasicRect
from special_r.Scene import Scene


class Pyramid:
    def __init__(self, x, y, w, h, scale=0.9, x_t=0, y_t=0, height=5):
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

        self.rects = []
        self.updates_rects()


    def updates_rects(self):
        scale_v = 1
        s_x, s_y = 0, 0
        c = [(73, 73, 71) for _ in range(self.height - 1)] + [(144, 255, 220)]

        for n in range(self.height):
            x = self.x + self.w * s_x
            y = self.y + self.w * s_x
            self.rects.append(BasicRect(x, y, self.w*scale_v, self.h*scale_v, color=c[n]))

            scale_v *= self.scale
            s_x += scale_v * self.x_t
            s_y += scale_v * self.x_t

    def update(self, ts):
        for r in self.rects:
            r.update(ts)

    def draw(self, surface):
        for r in self.rects:
            r.draw(surface)


def simple():
    x, y = 400, 400.
    w, h = 401., 201.

    # r = BasicRect(x, y,  w, h, 0, color=(13, 0, 255))
    # r2 = BasicRect(x, y, x, y, w + 4, h + 4, 0, color=(0, 0, 0))

    p = Pyramid(x, y, w, h, scale=0.8, x_t= 0.1, height=8)
    p2 = Pyramid(200., 200., 100., 200., scale=0.5, x_t=0.6, height=3)
    s = Scene([p, p2])

    s.animate(0)


if __name__ == '__main__':
    simple()
