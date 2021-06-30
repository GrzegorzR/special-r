import sys
from pygame.locals import *
from special_r.BasicRect import *

if __name__ == '__main__':
    pygame.init()

    FPS = 60.

    clock = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((900, 900))

    rs = []
    x, y = 400., 300.
    xp, yp = x, y - 20.
    r = BasicRect(x, y, xp, yp, 20., 60., math.pi, (0, 55, 255))

    c, unpin_n = 1, 0
    while True:
        # print(c, r.vr, math.sin(r.r), math.cos(r.r), r.r)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP:
                r.unpin()
        DISPLAYSURF.fill((92, 92, 138))

        r.update(20. / FPS)
        r.draw(DISPLAYSURF)
        pygame.display.update()
        c += 1
        # 123 480, 165 117
        #print(c, r.r)
        if c == 155:
            target_s = math.sin(r.r + math.pi)
            target_c = math.cos(r.r+ math.pi)
            r.unpin()
            #r.gravity_dir = 1.
            print(r.vr)
            print(c)
        if not r.pinned:
            s = math.sin(r.r)
            cs = math.cos(r.r)
            dist = abs(s - target_s) + abs(cs - target_c)
            print(c, dist)
            if c > 100 and dist < 0.1:
                r.pin()
                print(r.vr)
                print(r.piv_points_arr[0][1])
                r.gravity_dir *= -1.
                c=0
        #print(r.piv_points_arr[0][0], c)
        # pygame.image.save(DISPLAYSURF, "out/{}.jpeg".format(str(c).zfill(4)))
        clock.tick(FPS)
