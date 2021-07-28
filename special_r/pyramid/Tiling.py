from math import pi
from special_r.Scene import Scene
from special_r.pyramid.Pyramid import PyramidMoving
from special_r.pyramid.StockPyramidsDrawer import StockPyramidsDrawer


class TilingRects:
    def __init__(self, sizes, positions, funs, colorsets, img_size, dt=0.2, border_size=2):
        self.border_size = border_size
        self.dt = dt
        self.small = 300, 300
        self.big_h = 300, 600
        self.big_w = 600, 300
        self.sizes = sizes
        self.positions = positions
        self.colorsets = colorsets
        self.pyms = []
        self.funs = funs
        self.img_size = img_size
        self.initlize_pyms()

    def initlize_pyms(self):
        for i in range(len(self.positions)):
            self.pyms.append(
                PyramidMoving(self.positions[i][0], self.positions[i][1],
                              self.sizes[i][0], self.sizes[i][1],
                              self.funs[i], colors=self.colorsets[i],
                              scale=0.8, anim_param=20, height=10, border=self.border_size)
            )

    def animate(self, dt, out_dir):
        steps = self.calculate_steps_num(dt)
        p = StockPyramidsDrawer(self.pyms)
        s = Scene([p], bg_color=(0, 0, 0), img_size=self.img_size)
        s.animate(dt, output_dir=out_dir, save_range=(0, steps))

    def calculate_steps_num(self, dt):
        return 16 * pi / dt
