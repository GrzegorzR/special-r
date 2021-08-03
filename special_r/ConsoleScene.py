import itertools
import os
import pygame
from math import pi, sin, cos
from numpy import tanh
from pygame.locals import *

from special_r.Scene import Scene
from special_r.pyramid.Pyramid import PyramidMoving
from special_r.pyramid.StockPyramidsDrawer import StockPyramidsDrawer
from special_r.utils.colorsets import *
from special_r.utils.game_console import Console
from special_r.utils.parametric_functions import ParametricSegment




class ConsolePyramid(PyramidMoving):

    def __init__(self, x, y, w, h, height, scale, colors):

        self.height_fun = lambda t: height
        self.scale_fun = lambda t: scale
        super().__init__(x, y, w, h, move_fun, colors, scale=.85, border=2.)

    def change_xyt(self, x1, y1, translation_time=10.):
        x0, y0 = self.x_t, self.y_t
        t0, t1 = self.t, self.t + translation_time

        transition_fun_x = create_transition_fun(x0, x1, t0, t1)
        transition_fun_y = create_transition_fun(y0, y1, t0, t1)
        self.move_fun = lambda t: (transition_fun_x(t), transition_fun_y(t))

    def change_xt(self, x1, translation_time=10.):
        self.change_xyt(x1, self.y_t, translation_time)

    def change_yt(self, y1, translation_time=10.):
        self.change_xyt(self.x_t, y1, translation_time)

    def change_height(self, h1, translation_time=15):
        h0 = self.height
        t0, t1 = self.t, self.t + translation_time

        transition_fun_h = create_transition_fun(h0, h1, t0, t1)
        self.move_h = lambda t: round(transition_fun_h(t))

    def change_scale(self, s1, translation_time=10):
        s0 = self.scale
        t0, t1 = self.t, self.t + translation_time

        transition_fun_h = create_transition_fun(s0, s1, t0, t1)
        self.scale_fun = lambda t: transition_fun_h(t)

    def update(self, ts):
        self.height = self.height_fun(self.t)

        self.scale = self.scale_fun(self.t)
        super().update(ts)





class ConsoleScene:
    # takes Rects, and animations parameters
    # outputs animation as gif, series of png or live in window
    def __init__(self, objects=[], img_size=(800, 800), bg_color=(92, 92, 10)):
        self.objects = objects
        self.img_size = img_size
        self.bg_col = bg_color
        self.exit = False
        console_config = self.get_console_config()
        self.console = Console(self, img_size[1], console_config)

    def update_rule(self):
        pass

    def change_h(self, h):
        self.objects[0].height = h

    def animate(self, dt=0.005, output_dir=None, fps=60, save_range=None):
        if output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        pygame.init()

        if not dt:
            dt = 1. / fps

        clock = pygame.time.Clock()

        screen = pygame.display.set_mode(self.img_size)

        c, unpin_n = 1, 0
        while not self.exit:
            self.update_rule()
            events = pygame.event.get()

            for event in events:
                if event.type == QUIT:
                    self.exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self.exit = True
                elif event.type == pygame.KEYUP:
                    # Toggle console on/off the console
                    if event.key == pygame.K_F12:
                        self.console.toggle()

            self.update_bg(screen)
            for r in self.objects:
                r.update(dt)
                r.draw(screen)

            self.console.update(events)



            # Display the console if enabled or animation is still in progress

            self.console.show(screen)
            pygame.display.update()

            if output_dir:
                if not c % 100:
                    print(f'{c}/{save_range[1]}')
                pygame.image.save(screen, "{}/pym{}.png".format(output_dir, str(c).zfill(4)))
                c+=1
                if c >= save_range[1]:
                    return
            clock.tick(30)

    def save_imgs(self, steps):

        pass

    def display(self):
        pass

    def update_bg(self, surface):
        surface.fill(self.bg_col)

    def get_console_config(self):
        return {
            'global': {
                'layout': 'INPUT_BOTTOM',
                'padding': (10, 10, 10, 10),
                'bck_alpha': 150,
                # 'welcome_msg' : 'Sample 6: Mimimal - only input and output, with transparency and welcome msg\n***************\nType "exit" to quit\nType "help"/"?" for help\nType "? shell" for examples of python commands',
                'welcome_msg_color': (0, 255, 0)
            },
            'input': {
                'font_file': 'fonts/JackInput.ttf',
                'bck_alpha': 0
            },
            'output': {
                'font_file': 'fonts/JackInput.ttf',
                'bck_alpha': 0,
                'display_lines': 10,
                'display_columns': 100
            }
        }


def scene_console_simple():
    out_dir = None
    c = vienna_wom
    w, h = 200, 200
    height = 15
    dt = 0.2
    scale = 0.90
    steps = 16 * pi / dt
    # print(steps, dt)
    x = 400
    y = 400
    fun = ParametricSegment()

    p = ConsolePyramid(x, y, w, h, height, scale, colors=c)

    pyramides = []
    pyramides.append(p)

    s = ConsoleScene([p], bg_color=c[1])
    s.animate(dt, output_dir=out_dir, save_range=(0, steps))

def scene_states():
    out_dir = 'out/pym_18'
    #out_dir = None
    colors = vienna_wom

    w, h = 200, 200
    height = 15
    dt = 0.1
    scale = 0.93
    steps = (7./dt)*5*2
    x = 400
    y = 400
    colors = white_to_green(height+1)
    transition_time = 7.
    states = [(0.2, 0.2), (-0.2, 0.2),(0.2, -0.2),
              (-0.2, -0.2), (0.,0.)]
    p = StatePym(x, y, w, h, states, transition_time, height, scale, colors[1:])

    pyramides = []
    pyramides.append(p)
    s = ConsoleScene([p], bg_color=colors[0])
    s.animate(dt, output_dir=out_dir, save_range=(0, steps))





if __name__ == '__main__':
    scene_states()

