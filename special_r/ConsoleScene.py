import os
import pygame
from math import pi
from pygame.locals import *

from special_r.pyramid.Pyramid import PyramidMoving
from special_r.pyramid.StockPyramidsDrawer import StockPyramidsDrawer
from special_r.utils.colorsets import vienna_wom
from special_r.utils.game_console import Console
from special_r.utils.parametric_functions import ParametricSegment


class ConsoleScene:
    # takes Rects, and animations parameters
    # outputs animation as gif, series of png or live in window
    def __init__(self, objects=[], img_size=(900, 900), bg_color=(92, 92, 10)):
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

    def animate(self, dt=0.01, output_dir=None, fps=60, save_range=None):
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
                if event.type == QUIT: self.exit = True
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


if __name__ == '__main__':
    out_dir = None
    c = vienna_wom
    w, h = 200, 200
    pyramides = []

    dt = 0.2
    steps = 16 * pi / dt
    # print(steps, dt)
    x = 400
    y = 400
    fun = ParametricSegment()

    p = PyramidMoving(x, y, w, h, fun, colors=c, scale=0.8, anim_param=10, height=10)

    pyramides.append(p)

    s = ConsoleScene([p], bg_color=c[1])
    s.animate(dt, output_dir=out_dir, save_range=(0, steps))