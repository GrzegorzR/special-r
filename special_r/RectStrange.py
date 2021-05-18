import math
import sys
import numpy as np
import pygame
from pygame.locals import *


BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class RectStrange:
    def __init__(self, x, y, xp, yp, w, h, r, color=(0, 0, 255)):
        self.center = np.array([x, y])
        self.xp, self.yp = xp, yp
        self.xo, self.yo = x - xp, yp - y
        self.ver_points_mat = np.array([[w / 2., h / 2.], [w / 2., - h / 2.], [-w / 2., -h / 2.], [-w / 2., h / 2.]])
        self.piv_points_mat = np.array([[self.xo, self.yo], [self.xo, -self.yo], [0, 0]])

        self.update_postions_arrays()

        self.vr = 0.1
        self.ar = 0
        self.r = r
        self.l = h / 2. + abs(y - yp)
        self.v = np.array([0, 0])
        self.rotation_fraction = 1
        self.pinned = True
        self.w, self.h = w, h
        self.a = np.array([0, 0])
        self.color = color

        rot_matrix = self.get_rotation_matrix(r)

        points_tmp = np.pad(self.ver_points_arr, ((0, 0), (0, 1)), constant_values=1)
        self.ver_points_arr = np.dot(rot_matrix, points_tmp.T)[:2, :].T

        points_tmp = np.pad(self.piv_points_arr, ((0, 0), (0, 1)), constant_values=1)
        self.piv_points_arr = np.dot(rot_matrix, points_tmp.T)[:2, :].T

    def update_postions_arrays(self):

        self.ver_points_arr = np.tile(self.center, [4, 1]) + self.ver_points_mat
        self.piv_points_arr = self.center + self.piv_points_mat

    def get_rotation_matrix(self, r):
        r00, r01, r10, r11 = math.cos(r), math.sin(r), -math.sin(r), math.cos(r)
        rot_matrix = np.array([[r00, r01, self.xp - (r00 * self.xp) - (r01 * self.yp)],
                               [r10, r11, self.yp - (r10 * self.xp) - (r11 * self.yp)],
                               [0, 0, 1]])
        return rot_matrix

    def unpin(self):
        points_tmp = self.piv_points_arr
        # self.rotation_pivot = self.center
        # self.xp, self.yp = self.center[0], self.center[1]
        # v = np.cross(np.array([0, 0, self.vr]), np.array([points_tmp[1][0] - self.xp, points_tmp[1][1] - self.yp, 0]))
        v = np.cross(np.array([0, 0, self.vr]),
                     np.array([points_tmp[1][0] - self.xp, points_tmp[1][1] - self.yp, 0])) * 10
        # v = np.array([points_tmp[1][0] - v[0], points_tmp[1][1] - v[1]])*0.5

        # v = np.array([points_tmp[1][0] - v[0], points_tmp[1][1]- v[1]])
        # v = v * 3
        # tmp_v = self.vr * 100
        # vy = tmp_v * math.sin(math.pi / 2. - self.r)
        # vx = -tmp_v * math.sin(self.r)
        # rot_matrix = self.get_rotation_matrix(self.r)
        # points_tmp = np.pad(self.center, ((0, 1)), constant_values=1)
        # print(self.center)
        # self.center = np.dot(rot_matrix, np.array([points_tmp]).T)[:2, 0]

        self.xp, self.yp = self.center[0], self.center[1]
        self.v = np.array([0, 0])
        self.ar = 0
        self.a = np.array([-0.5, 0.])
        self.pinned = False

    def pin(self):
        self.pinned = True
        self.v = np.array([0, 0])
        self.a = np.array([0, 0])

        rot_matrix = self.get_rotation_matrix(self.r)

        points_tmp = np.pad(self.piv_points_arr, ((0, 0), (0, 1)), constant_values=1)
        points_tmp = np.dot(rot_matrix, points_tmp.T)[:2, :]
        self.xp, self.yp = points_tmp[0][0], points_tmp[1][0]

    def update(self, ts):

        self.vr += self.ar * ts
        self.vr *= self.rotation_fraction
        dr = round(self.vr * ts, 5)
        self.r += dr

        self.v[0] += self.a[0] * ts
        self.v[1] += self.a[1] * ts
        self.center[0] += self.v[0] * ts
        self.center[1] += self.v[1] * ts

        #
        # strange spring effect here
        self.update_postions_arrays()

        if not self.pinned:
            print(self.center, self.a * ts, self.v,self.a[0] * ts)
            self.xp, self.yp = self.center[0], self.center[1]
        rot_matrix = self.get_rotation_matrix(dr)
        # print(self.r)
        #self.piv_points_arr[2][0] = self
        # self.ver_points_arr = np.tile(self.center, [4, 1]) + self.ver_points_mat
        points_tmp = np.pad(self.ver_points_arr, ((0, 0), (0, 1)), constant_values=1)
        self.ver_points_arr = np.dot(rot_matrix, points_tmp.T)[:2, :].T

        # self.piv_points_arr = np.tile(self.center, [2, 1]) + self.piv_points_mat
        points_tmp = np.pad(self.piv_points_arr, ((0, 0), (0, 1)), constant_values=1)
        self.piv_points_arr = np.dot(rot_matrix, points_tmp.T)[:2, :].T

        self.center = np.array([self.piv_points_arr[2][0], self.piv_points_arr[2][1]])

        if self.pinned:
            self.ar = -math.sin(self.r) * 0.01

    def draw(self, surface):
        points_tmp = self.piv_points_arr
        # rot_matrix = self.get_rotation_matrix(self.r)
        v = np.cross(np.array([0, 0, self.vr]),
                     np.array([points_tmp[1][0] - self.xp, points_tmp[1][1] - self.yp, 0])) * 10
        pygame.draw.line(surface, BLACK, (points_tmp[1][0], points_tmp[1][1]),
                         (points_tmp[1][0] - v[0], points_tmp[1][1]), width=1)
        pygame.draw.line(surface, BLACK, (points_tmp[1][0], points_tmp[1][1]),
                         (points_tmp[1][0], points_tmp[1][1] - v[1]), width=1)
        # pygame.draw.line(surface, BLACK, (points_tmp[1][0], points_tmp[1][1]),
        #                 (v[0], v[1]), width=1)
        # print(points_tmp[1][0] -v[0], points_tmp[1][1]- v[1])
        pygame.draw.polygon(surface, self.color, self.ver_points_arr)
        # print (v)

        pygame.draw.circle(surface, RED, (points_tmp[1][0], points_tmp[1][1]), 2)
        pygame.draw.circle(surface, RED, (points_tmp[0][0], points_tmp[0][1]), 2)

        pygame.draw.circle(surface, GREEN, (points_tmp[2][0], points_tmp[2][1]), 2)

if __name__ == '__main__':
    pygame.init()

    FPS = 30
    clock = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((900, 900))

    rs = []
    for i in range(10):
        x = 50. + 85 * i
        y = 450
        xp, yp = x, y - 20
        w, h = 20, 60
        rs.append(RectStrange(x, y, xp, yp, w, h, i*0.2, (0, i * 20 % 255, 255)))
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

        #pygame.image.save(DISPLAYSURF, "out/{}.jpeg".format(str(c).zfill(4)))
        clock.tick(FPS)