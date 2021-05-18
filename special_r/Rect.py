import math
import numpy as np
import pygame
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Rect:
    def __init__(self, x, y, xp, yp, w, h, r, color=(0, 0, 255)):
        self.center = np.array([x, y])
        # self.rotation_pivot = np.array([x+xp, x+yp])
        self.xp, self.yp = xp, yp
        self.xo, self.yo = x - xp, yp - y
        self.ver_points_mat = np.array([[w / 2., h / 2.], [w / 2., - h / 2.], [-w / 2., -h / 2.], [-w / 2., h / 2.]])
        self.piv_points_mat = np.array([[self.xo, self.yo], [self.xo, -self.yo], [0, 0]])
        self.gravity_dir = 1.
        self.update_postions_arrays()
        self.points_to_print = []
        self.vr = 0.05
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

        self.v = -np.cross(np.array([0, 0, self.vr]),
                           np.array([self.center[0] - self.xp, self.center[1] - self.yp, 0]))[:2] * 1
        self.ar = 0
        self.xp, self.yp = self.center[0], self.center[1]
        self.a = np.array([0., 0.1])
        self.pinned = False
        self.rotation_fraction = 1

    def pin(self):
        self.pinned = True
        self.v = np.array([0., 0.])
        self.a = np.array([0., 0.])

        # rot_matrix = self.get_rotation_matrix(self.r)

        self.xp, self.yp = self.piv_points_arr[0][0], self.piv_points_arr[0][1]
        self.rotation_fraction = 1.

    def update_position(self, ts):

        ts = float(ts)
        self.v = self.v + (self.a * float(ts) * self.gravity_dir)

        ds = self.v * ts
        self.center += ds

        self.ver_points_arr += ds
        self.piv_points_arr += ds

    def update_rotation(self, ts):

        self.vr += self.ar * ts
        self.vr *= self.rotation_fraction
        dr = round(self.vr * ts, 5)
        self.r += dr
        self.points_to_print.append([self.piv_points_arr[0][0], self.piv_points_arr[0][1]])
        if not self.pinned:
            self.xp, self.yp = self.center[0], self.center[1]

        rot_matrix = self.get_rotation_matrix(dr)
        points_tmp = np.pad(self.ver_points_arr, ((0, 0), (0, 1)), constant_values=1)
        self.ver_points_arr = np.dot(rot_matrix, points_tmp.T)[:2, :].T

        points_tmp = np.pad(self.piv_points_arr, ((0, 0), (0, 1)), constant_values=1)
        self.piv_points_arr = np.dot(rot_matrix, points_tmp.T)[:2, :].T

        self.center = np.array([self.piv_points_arr[2][0], self.piv_points_arr[2][1]])

        if self.pinned:
            self.ar = -math.sin(self.r) * 0.01 * self.gravity_dir

    def update(self, ts):
        ts = float(ts)

        self.update_position(ts)
        self.update_rotation(ts)

    def draw(self, surface):
        points_tmp = self.piv_points_arr
        # rot_matrix = self.get_rotation_matrix(self.r)
        v = np.cross(np.array([0, 0, self.vr]),
                     np.array([points_tmp[1][0] - self.xp, points_tmp[1][1] - self.yp, 0])) * 10
        # pygame.draw.line(surface, BLACK, (points_tmp[1][0], points_tmp[1][1]),
        #                 (points_tmp[1][0] - v[0], points_tmp[1][1]), width=1)
        # pygame.draw.line(surface, BLACK, (points_tmp[1][0], points_tmp[1][1]),
        #                 (points_tmp[1][0], points_tmp[1][1] - v[1]), width=1)
        # pygame.draw.line(surface, BLACK, (points_tmp[1][0], points_tmp[1][1]),
        #                 (v[0], v[1]), width=1)
        # print(points_tmp[1][0] -v[0], points_tmp[1][1]- v[1])
        for p in self.points_to_print:
            # print(p)
            # pygame.draw.circle(surface, RED, (p[0], p[1]), 1)
            pass
        pygame.draw.polygon(surface, self.color, self.ver_points_arr)

        # pygame.draw.circle(surface, RED, (points_tmp[1][0], points_tmp[1][1]), 2)
        #pygame.draw.circle(surface, (247, 122, 59), (points_tmp[0][0], points_tmp[0][1]), 4)

        # pygame.draw.circle(surface, GREEN, (points_tmp[2][0], points_tmp[2][1]), 2)
