import copy
import sys
from pygame.locals import *

from special_r.BasicRect import *
from special_r.BasicRect import BasicRect



class SimulatorUnpin:
    def __init__(self, r, max_iter=200, update_rate=0.5):
        self.r = r
        self.max_iter = max_iter
        self.update_rate = update_rate


    def solve(self, x,y):
        best_t = 0
        target = np.array([x, y])
        best_dist = np.linalg.norm(target - self.r.center)
        for t in range(self.max_iter):
            self.r.update(self.update_rate)
            r_tmp = copy.deepcopy(self.r)
            r_tmp.unpin()
            for i in range(500):
                r_tmp.update(self.update_rate)
                piv_point = np.array([r_tmp.piv_points_arr[0][0], r_tmp.piv_points_arr[0][1]])
                dist_tmp = np.linalg.norm(target - piv_point)
                if dist_tmp < 1:
                    print(dist_tmp, self.r.r)
                if dist_tmp < best_dist:
                    #print(t)
                    best_dist = dist_tmp
                    best_t = self.r.r

        print(best_dist, best_t)

class SimulatorPin:
    def __init__(self, r, max_iter=200, update_rate=0.5):
        self.r = r
        self.max_iter = max_iter
        self.update_rate = update_rate

    def solve(self):
        initial_y = self.r.piv_points_arr[0][1]
        best_dist = 2.
        for t in range(self.max_iter):
            self.r.update(self.update_rate)
            initial_r = self.r.r
            target_s = math.sin(initial_r + math.pi/2.)
            target_c = math.cos(initial_r + math.pi/2.)
            r_tmp = copy.deepcopy(self.r)
            r_tmp.unpin()
            #print(t, initial_r)
            #print(t)
            for i in range(1000):
                #print(t,i, )
                r_tmp.update(self.update_rate)
                piv_point = np.array([r_tmp.piv_points_arr[0][0], r_tmp.piv_points_arr[0][1]])
                #print(piv_point, initial_y)
                if math.isclose(piv_point[1], initial_y, abs_tol=0.5) and i >100:

                    s = math.sin(r_tmp.r)
                    c = math.cos(r_tmp.r)
                    dist = abs(s - target_s) + abs(c - target_c)
                    #print(piv_point, initial_y, math.isclose(piv_point[0], initial_y, abs_tol=1.))
                    #print(t,i)
                    if dist < best_dist:
                        #print(t)
                        best_dist = dist
                        best_r = initial_r
                        best_t = t
                        print(best_dist, best_t, best_r, r_tmp.r, piv_point, r_tmp.piv_points_arr[0][1], i)

        print(best_dist, best_t, best_r, initial_r)



def sim_1():
    pygame.init()

    FPS = 60

    clock = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((900, 900))

    rs = []
    x, y = 400., 300.
    xp, yp = x, y - 20.
    r = BasicRect(x, y, xp, yp, 20., 60., math.pi, (0, 55, 255))
    c, unpin_n = 1, 0
    while True:
        # print(c, r.vr, math.sin(r.r), math.cos(r.r))
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
        if math.isclose(math.sin(r.r), math.sin(math.pi * 0.25), abs_tol=0.05) and r.pinned and c < 100:
            r.unpin()
            r.gravity_dir = 1.
            print(r.r)
        if math.isclose(-math.sin(r.r), 0.61, abs_tol=0.1) \
                        and math.isclose(math.cos(r.r), 0.78,abs_tol=0.1)\
                        and not r.pinned:

            r.pin()
            r.gravity_dir = -1
            s = SimulatorUnpin(r, max_iter=100, update_rate=20. / FPS)
            s.solve(xp, yp)

        # pygame.image.save(DISPLAYSURF, "out/{}.jpeg".format(str(c).zfill(4)))
        clock.tick(FPS)

def sim_2():
    pygame.init()

    FPS = 60.

    clock = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((900, 900))
    x, y = 400., 300.
    xp, yp = x, y - 20.
    r = BasicRect(x, y, xp, yp, 20., 60., math.pi, (0, 55, 255))


    simulator = SimulatorPin(r, update_rate=20. / FPS)
    simulator.solve()

    c, unpin_n = 1, 0
    while True:
        # print(c, r.vr, math.sin(r.r), math.cos(r.r))
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
        if c == 67:
            r.unpin()
            r.gravity_dir = 1.
            print(r.r)
        if math.isclose(-math.sin(r.r), 0.61, abs_tol=0.1) \
                and math.isclose(math.cos(r.r), 0.78, abs_tol=0.1) \
                and not r.pinned:
            r.pin()
            r.gravity_dir = -1
            s = SimulatorUnpin(r, max_iter=100, update_rate=20. / FPS)
            s.solve(xp, yp)

        # pygame.image.save(DISPLAYSURF, "out/{}.jpeg".format(str(c).zfill(4)))
        clock.tick(FPS)


if __name__ == '__main__':
    sim_2()






