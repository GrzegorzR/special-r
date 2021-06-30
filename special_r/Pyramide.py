import numpy as np
import pygame

from special_r.BasicRect import BasicRect
from special_r.Scene import Scene

class Piramide:
    def __init__(self):
        self.x, self.y = 400, 400


        self.rects = [BasicRect (y + i*2,x + i*2, i*50 +1, i*20 + 1) for i in reversed(range(5, 10))]

    def update(self, ts):
        pass

    def draw(self, surface):
        for r in self.rects:
            r.draw(surface)

def simple():
    x,y = 400, 400.
    w,h = 51., 101.

    r = BasicRect(x, y,  w, h, 0, color=(13, 0, 255))
    #r2 = BasicRect(x, y, x, y, w + 4, h + 4, 0, color=(0, 0, 0))

    p = Piramide()
    s = Scene([ p], None)

    s.animate(0)


if __name__ == '__main__':
    simple()
