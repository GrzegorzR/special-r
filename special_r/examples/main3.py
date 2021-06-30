import sys
from pygame.locals import *
from special_r.BasicRect import *
from special_r.PinRect import PinRect

if __name__ == '__main__':
    pygame.init()

    FPS = 60
    clock = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((900, 900))

    rs = []
    for i in range(10):
        x = 50. + 85 * i
        y = 450
        xp, yp = x, y - 20
        w, h = 20, 60
        rs.append(PinRect(x, y, w, h, xp, yp,  i * 20., color=(0, i * 20 % 255, 255)))
    c, unpin_n = 1, 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP:
                rs[unpin_n].unpin()
                unpin_n += 1

        DISPLAYSURF.fill((92, 92, 10))
        for r in rs:
            r.update(20./FPS)
            r.draw(DISPLAYSURF)
        pygame.display.update()
        c += 1
        #pygame.display.update()

        pygame.image.save(DISPLAYSURF, "out/{}.jpeg".format(str(c).zfill(4)))
        clock.tick(FPS)
