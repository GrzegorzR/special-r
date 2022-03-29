import glob
import os
from math import sin,cos, pi
from special_r.BasicRect import BasicRect
from special_r.Scene import Scene


class HideRect(BasicRect):
    def __init__(self, x, y, w, h, color, hide_range):
        super().__init__(x, y, w, h, color=color)
        self.hide_range = hide_range
        self.const_color = color
        self.t = 0

    def update(self, ts):
        # print(sin(self.t))
        if self.hide_range[0] * sin(self.t * pi) >0 and self.hide_range[1]* cos(self.t * pi) >0:
            self.color = None
        else:
            self.color = self.const_color
        self.t += ts
        super(HideRect, self).update(ts)


def fun():
    w, h = 800, 800

    rects = []
    rects.append(HideRect(w / 2 + 100, h / 2 - 100, 160, 160, (21, 11, 1), (1., 1)))
    rects.append(HideRect(w / 2 + 100, h / 2 + 100, 160, 160, (21, 11, 1), (1., -1.)))
    rects.append(HideRect(w / 2 - 100, h / 2 + 100, 160, 160, (21, 11, 1), (-1., -1.)))
    rects.append(HideRect(w / 2 - 100, h / 2 - 100, 160, 160, (21, 11, 1), (-1., 1.)))

    s = Scene(rects, (w, h))
    output_dir = 'out/music_sync_test'
    #output_dir = None
    files = glob.glob('{}/*'.format(output_dir))

    if output_dir:
        for f in files:
            os.remove(f)

    s.animate(1 / 60, output_dir, save_range=(0, 8 * 60))


if __name__ == '__main__':
    fun()
