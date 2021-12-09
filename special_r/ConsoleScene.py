import itertools
import os
import pygame
from math import pi, sin, cos
from numpy import tanh
from pygame.locals import *
import pygame.freetype
from special_r.Scene import Scene
from special_r.pyramid.Pyramid import PyramidMoving
from special_r.pyramid.StockPyramidsDrawer import StockPyramidsDrawer
from special_r.utils.colorsets import *
from special_r.utils.game_console import Console
from special_r.utils.parametric_functions import ParametricSegment

pygame.freetype.init()


class ConsoleScene:
    # takes Rects, and animations parameters
    # outputs animation as gif, series of png or live in window
    def __init__(self, objects=[], img_size=(800, 800), bg_color=(92, 92, 10)):
        self.objects = objects
        self.img_size = img_size
        self.bg_col = bg_color
        self.exit = False
        console_config = self.get_console_config()
        self.console = Console(self, img_size[0], console_config)

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

        screen = pygame.display.set_mode(self.img_size, pygame.FULLSCREEN)

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
                c += 1
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
                'font_size': 50,
                # 'welcome_msg' : 'Sample 6: Mimimal - only input and output, with transparency and welcome msg\n***************\nType "exit" to quit\nType "help"/"?" for help\nType "? shell" for examples of python commands',
                'welcome_msg_color': (0, 255, 0)
            },
            'input': {
                'font_file': 'fonts/JackInput.ttf',
                'bck_alpha': 0,
                'font_size': 50
            },
            'output': {
                'font_file': 'fonts/JackInput.ttf',
                'bck_alpha': 0,
                'display_lines': 6,
                'display_columns': 100,
                'font_size': 30
            }
        }


class TextObj:
    def __init__(self, ob, pos, update_fun):
        self.pos = pos
        self.ob = ob
        self.font = pygame.freetype.Font('fonts/miscfs.ttf', 35)
        self.text = 'abc'
        self.update_fun = update_fun

    def draw(self, screen):
        text_surface, rect = self.font.render(self.text, (0, 0, 0))
        rect.left = self.pos[0]
        rect.top = self.pos[1]
        screen.blit(text_surface, rect)

    def update(self, dt):
        self.text = self.update_fun(self.ob)


class TextScale(TextObj):
    def update(self, dt):
        self.text = f'scale: {self.ob.scale:.2f}'


class TextXY(TextObj):
    def update(self, dt):
        self.text = f'x_t: {self.ob.x_t:.2f}/n' \
                    f'y_t: {self.ob.y_t:.2f}'


class ConsolePym(PyramidMoving):
    def __init__(self, x, y, w, h, move_fun, colors_fun, borders_colors_fun=None, scale=0.99, height=20, anim_param=1.,
                 vr=0.0, border=2.):
        self.colors_fun = colors_fun
        self.height = height
        if not borders_colors_fun:
            self.borders_colors_fun = lambda l: [(0, 0, 0) for _ in range(l)]
        else:
            self.borders_colors_fun = borders_colors_fun
        self.update_color()
        super().__init__(x, y, w, h, move_fun, self.colors, scale, height, anim_param, vr, border)

    def update_color(self):
        self.colors = self.colors_fun(self.height)
        self.borders_colors = self.borders_colors_fun(self.height)

    def update(self, ts):
        self.rects = []
        self.height = self.height_fun(self.t)
        self.scale = self.scale_fun(self.t)
        self.x_t, self.y_t = self.xyt_fun(self.t)
        self.update_color()
        self.x_t, self.y_t = self.x_t / self.animation_parameter, self.y_t / self.animation_parameter
        self.updates_rects()
        super().update(ts)
        self.t += ts


def scene_console_simple():
    out_dir = 'out/change_s_test'
    out_dir = None
    colors = vienna_wom
    w, h = 700, 700
    height = 15
    dt = 0.2
    scale = 0.86
    steps = 16 * pi / dt
    # print(steps, dt)
    x = 400
    y = 400
    fun = ParametricSegment()
    fun = lambda t: (sin(t / 10.) / 20., 0)
    colors = white_to_red(25)
    colors = white_to_green(25)[4:]
    colors_fun = lambda height: [(255, 255, 255) for _ in range(height - 1)] + [(40, 40, 0), (40, 40, 0)]
    p = ConsolePym(x, y, w, h, fun, colors, scale=scale, border=2)
    p.scale_fun = lambda t: 0.9 + sin(t / 5.) / 15.
    t_scale = TextObj(p, (550, 600), lambda ob: f'scale: {ob.scale:.2f}')
    t_x = TextObj(p, (550, 650), lambda ob: f'x_t: {ob.x_t:.2f}')
    t_y = TextObj(p, (550, 700), lambda ob: f'y_t: {ob.y_t:.2f}')
    t_h = TextObj(p, (550, 750), lambda ob: f'height: {ob.height}')

    pyramides = []
    pyramides.append(p)

    s = ConsoleScene([p, t_x, t_y, t_scale, t_h], bg_color=colors[0])
    s.animate(dt, output_dir=out_dir, save_range=(0, 9000))


def scene_show_parameters():
    #$out_dir = 'out/scene_1/scene_change_parameters'
    out_dir = None
    w, h = 400, 400
    dt = 0.2
    scale = 0.78
    steps = 16 * pi / dt
    img_size = (1920, 1080)
    # print(steps, dt)
    height = 1
    x = 600
    y = 600
    fun = lambda t: (0, 0)
    dark_red = '#380200'
    colors_fun = lambda height: [(255, 255, 255) for _ in range(height - 1)] + [dark_red, dark_red]
    grey = '#EBE6E6'
    black = '#121717'
    border_colors_fun = lambda l : colors_range_hex(Color(black), Color(grey), l)
    p = ConsolePym(x, y, w, h, fun, colors_fun, borders_colors_fun=border_colors_fun,
                   height=height, scale=scale, border=2)

    text_pos_x, text_pos_y = x+300, y-200

    t_h = TextObj(p, (text_pos_x, text_pos_y), lambda ob: f'height: {ob.height}')
    t_scale = TextObj(p, (text_pos_x, text_pos_y + 50), lambda ob: f'scale: {ob.scale:.2f}')
    t_x = TextObj(p, (text_pos_x, text_pos_y + 100), lambda ob: f'x_t: {ob.x_t:.2f}')
    t_y = TextObj(p, (text_pos_x, text_pos_y + 150), lambda ob: f'y_t: {ob.y_t:.2f}')

    pyramides = []
    pyramides.append(p)

    s = ConsoleScene([p, t_x, t_y, t_scale, t_h], img_size=img_size, bg_color='#82808A')
    s.animate(dt, output_dir=out_dir, save_range=(0, 9000))


if __name__ == '__main__':
    # print(pygame.font.get_fonts())
    # scene_console_simple()
    scene_show_parameters()
