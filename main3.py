import sys
from pygame.locals import *
from special_r.Rect import *



if __name__ == '__main__':
    pygame.init()

    FPS = 30
    clock = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((900, 900))

    rs = []
    for i in range(1):
        x = 50. + 85 * i
        y = 450
        xp, yp = x, y - 20
        w, h = 20, 60
        rs.append(Rect(x, y, xp, yp, w, h, i * 20., (0, i * 20 % 255, 255)))
    c, unpin_n = 1, 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP:
                rs[unpin_n].unpin()
                unpin_n += 1

        DISPLAYSURF.fill((92, 92, 138))
        for r in rs:
            r.update(1)
            r.draw(DISPLAYSURF)
        pygame.display.update()
        c += 1
        pygame.display.update()

        pygame.image.save(DISPLAYSURF, "out/{}.jpeg".format(str(c).zfill(4)))
        clock.tick(FPS)
