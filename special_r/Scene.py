import os
import sys
import numpy
import pygame
from pygame.locals import *


class Scene:
    # takes Rects, and animations parameters
    # outputs animation as gif, series of png or live in window
    def __init__(self, objects, img_size=(900, 800), bg_color=(255, 255, 255)):
        self.objects = objects
        self.img_size = img_size
        self.bg_col = bg_color
        self.c = 0
        self.t = 0

    def update_rule(self, dt=0.1):
        pass

    def post_update_rule(self):
        pass

    def animate(self, dt=0, output_dir=None, fps=60, save_range=None):
        if not save_range:
            save_range = (0,100000)
        if output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                initial_num = 0
            else:
                initial_num = len(os.listdir(output_dir))
        pygame.init()

        if not dt:
            dt = 1. / fps

        #clock = pygame.time.Clock()
        if not output_dir:
            screen = pygame.display.set_mode(self.img_size)
        else:
            screen = pygame.Surface(self.img_size)

        unpin_n = 0
        while True:
            self.t += dt
            self.update_rule(dt)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.update_bg(screen)
            #self.update_objects(dt)
            #self.draw_objects(screen)
            for r in self.objects:
                r.update(dt)
                r.draw(screen)
            self.post_update_rule()
            self.c += 1
            if self.c > save_range[1]:
                return
            if not self.c % 100:
                print(f'{self.c}/{save_range[1]}')
                #pass
            if output_dir:
                if save_range:
                    if save_range[0] <= self.c <= save_range[1]:
                        pygame.image.save(screen,
                                          "{}/pym{}.png".format(output_dir, str(unpin_n + initial_num).zfill(4)))
                        unpin_n += 1
                else:
                    pygame.image.save(screen, "{}/pym{}.png".format(output_dir, str(self.c).zfill(4)))
            else:
                pygame.display.update()
            # clock.tick(10)

    def save_imgs(self, steps):

        pass

    def display(self):
        pass

    def update_bg(self, surface):
        surface.fill(self.bg_col)


class SceneBackground(Scene):
    def __init__(self, objects, background_img, img_size=1000):
        super().__init__(objects=objects, img_size=img_size)
        self.bg = pygame.image.load(background_img)

    def update_bg(self, surface):
        surface.blit(self.bg, (0, 0))
