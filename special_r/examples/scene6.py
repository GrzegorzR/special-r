import sys
from pygame.locals import *

from special_r.LoopRect import LoopRect
from special_r.BasicRect import *

if __name__ == '__main__':
    pygame.init()

    FPS = 60

    clock = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((900, 900))

    rs = []
    x, y = 400., 300.
    xp, yp = x, y - 20.
    rs = []
    for i in range(1,20):
        rs.append(LoopRect(x, y, xp, yp, 20., 60., math.pi, i / 2., color=(0, 55, i * 10)))

    c, unpin_n = 1, 0
    while True:
        # print(c, r.vr, math.sin(r.r), math.cos(r.r), r.r)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill((92, 92, 138))
        for r in rs:
            r.update(20. / FPS)
            r.draw(DISPLAYSURF)
        #print(r.pinned)

        pygame.display.update()
        #print(r.piv_points_arr[0][0], c)
        # pygame.image.save(DISPLAYSURF, "out/{}.jpeg".format(str(c).zfill(4)))
        clock.tick(FPS)
