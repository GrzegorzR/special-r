import sys
import pygame
from pygame.locals import *


class Scene():
    # takes Rects, and animations parameters
    # outputs animation as gif, series of png or live in window
    def __init__(self, objects=[], img_size=800, bg_color=(92, 92, 10)):
        self.objects = objects
        self.img_size = img_size
        self.bg_col = bg_color

    def update_rule(self):
        pass

    def animate(self, time):
        pygame.init()

        FPS = 60

        clock = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((self.img_size, self.img_size))

        c, unpin_n = 1, 0
        while True:
            self.update_rule()
            # pygame.image.save(DISPLAYSURF, "out/test/{}.png".format(str(c).zfill(4)))
            # print(c, r.vr, math.sin(r.r), math.cos(r.r), r.r)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            DISPLAYSURF.fill(self.bg_col)
            for r in self.objects:
                r.update(1. / float(FPS))
                r.draw(DISPLAYSURF)
            pygame.display.update()
            c += 1

            clock.tick(FPS)

    def save_imgs(self, steps):

        pass

    def display(self):
        pass
