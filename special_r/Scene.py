import sys
import pygame
from pygame.locals import *

class Scene():
    # takes Rects, and animations parameters
    # outputs animation as gif, series of png or live in window
    def __init__(self, objects, params):
        self.objects = objects
        self.params = params
        self.img_size = 800
        self.bg_col = (92, 92, 10)

    def animate(self, time):
        pygame.init()

        FPS = 25

        clock = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((self.img_size, self.img_size))



        c, unpin_n = 1, 0
        while True:
            pygame.image.save(DISPLAYSURF, "out/test/{}.png".format(str(c).zfill(4)))
            # print(c, r.vr, math.sin(r.r), math.cos(r.r), r.r)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            DISPLAYSURF.fill((92, 5, 10))
            for r in self.objects:
                r.update(0.4)
                r.draw(DISPLAYSURF)
            pygame.display.update()
            c += 1


            clock.tick(FPS)
