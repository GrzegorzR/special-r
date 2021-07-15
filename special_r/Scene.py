import os
import sys
import pygame
from pygame.locals import *


class Scene:
    # takes Rects, and animations parameters
    # outputs animation as gif, series of png or live in window
    def __init__(self, objects=[], img_size=900, bg_color=(92, 92, 10)):
        self.objects = objects
        self.img_size = img_size
        self.bg_col = bg_color

    def update_rule(self):
        pass

    def animate(self, dt=0, output_dir=None,  fps=60, save_range=None):
        pygame.init()

        if not dt:
            dt = 1./fps

        clock = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((self.img_size, self.img_size))

        c, unpin_n = 1, 0
        while True:
            self.update_rule()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            DISPLAYSURF.fill(self.bg_col)
            for r in self.objects:
                r.update(dt)
                r.draw(DISPLAYSURF)
            #pygame.display.update()
            c += 1
            if c > save_range[1]:
                return

            if output_dir:
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                if save_range:

                    if save_range[0] <= c <= save_range[1]:

                        pygame.image.save(DISPLAYSURF, "{}/pym{}.png".format(output_dir, str(unpin_n).zfill(4)))
                        unpin_n += 1
                else:
                    pygame.image.save(DISPLAYSURF, "{}/pym{}.png".format(output_dir, str(c).zfill(4)))


            clock.tick(20)

    def save_imgs(self, steps):

        pass

    def display(self):
        pass
