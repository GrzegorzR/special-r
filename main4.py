import sys
import random
from pygame.locals import *

from special_r.Rect import *


class RectSource:
    def __init__(self):
        self.counter = 0
        self.rects = []

    def add_rect(self):
        pass

    def update(self):
        for r in self.rects:
            r.update()

        self.counter += 1


class TestRectSrc(RectSource):
    def __init__(self, x, y, size, color):
        super().__init__()
        self.x, self.y = x, y
        self.size = size
        self.color = color

    def add_rect(self):
        self.rects.append(Rect(self.x, self.y, self.x, self.y + 15, 40, 10, random.random() * 5, self.color()))

def scene1():
    pygame.init()

    FPS = 6
    clock = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((900, 900))

    rs = []
    for i in range(10):
        x, y = 450., 150. + 50 * i
        xp, yp = x, y - 20
        w, h = 20, 100
        rs.append(Rect(x, y, xp, yp, w, h, 0.2 * i, (0, i * 20, 255)))
    c, unpin_n = 1, 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                for r in rs:
                    r.unpin()
        if not c % 15 and unpin_n < 10:
            rs[unpin_n].unpin()
            unpin_n += 1

        DISPLAYSURF.fill((92, 92, 138))
        for r in rs:
            r.update(1)
            r.draw(DISPLAYSURF)
        pygame.display.update()
        c += 1
        # print(c)
        clock.tick(FPS)

def scene2():
    pygame.init()

    FPS = 20
    clock = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((900, 900))

    rs = []
    for i in range(5):
        x, y = 450., 150. + 50 * i
        xp, yp = x, y - 20
        w, h = 20, 100
        rs.append(Rect(x, y, xp, yp, w, h, 0.2 * i, (0, i * 20, 255)))
    c, unpin_n = 1, 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                for r in rs:
                    r.unpin()
        if not c % 20 and unpin_n < len(rs):
            rs[unpin_n].unpin()
            unpin_n += 1

        #if c == 70:
        #    for r in rs:
        #        r.pin()

        DISPLAYSURF.fill((92, 92, 138))
        for r in rs:
            r.update(1)
            r.draw(DISPLAYSURF)
        pygame.display.update()
        c += 1
        pygame.image.save(DISPLAYSURF, "out/{}.jpeg".format(str(c).zfill(4)))
        # print(c)
        clock.tick(FPS)



if __name__ == '__main__':
    scene2()

