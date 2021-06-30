import math
import numpy as np
import pygame
import pygame.gfxdraw

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class BasicRect:
    def __init__(self, x, y,  w, h, xp=0, yp=0, r=0, vr=0.05, color=(0, 0, 255)):
        self.center = np.array([x, y])
        # self.rotation_pivot = np.array([x+xp, x+yp])
        #self.xp, self.yp = xp, yp
        if not xp and  not yp:
            self.xp, self.yp = x, y
        else:
            self.xp, self.yp = xp, yp
        self.xo, self.yo = x - xp, yp - y
        self.points_to_print = []
        self.vr = vr
        self.ar = 0
        self.r = r
        self.l = h / 2. + abs(y - yp)
        self.v = np.array([0, 0])
        self.rotation_fraction = 1
        self.w, self.h = w, h
        self.a = np.array([0, 0])
        self.color = color
        self.gravity_dir = 1
        self.diagonal_len = math.sqrt(w * w + h * h)
        self.border = 1.6

        self.ver_points_mat = np.array([[w / 2., h / 2.], [w / 2., - h / 2.], [-w / 2., -h / 2.], [-w / 2., h / 2.]])
        self.piv_points_mat = np.array([[self.xo, self.yo], [self.xo, -self.yo], [0, 0]])
        self.update_postions_arrays()

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

        rot_matrix = self.get_rotation_matrix(dr)
        points_tmp = np.pad(self.ver_points_arr, ((0, 0), (0, 1)), constant_values=1)
        self.ver_points_arr = np.dot(rot_matrix, points_tmp.T)[:2, :].T

        points_tmp = np.pad(self.piv_points_arr, ((0, 0), (0, 1)), constant_values=1)
        self.piv_points_arr = np.dot(rot_matrix, points_tmp.T)[:2, :].T

        self.center = np.array([self.piv_points_arr[2][0], self.piv_points_arr[2][1]])

    def update(self, ts):
        ts = float(ts)
        self.update_position(ts)
        self.update_rotation(ts)

    def draw(self, surface):
        # rot_matrix = self.get_rotation_matrix(self.r)



        if self.border:
            border_points = (self.border * (self.ver_points_arr- self.center  ) / (self.diagonal_len / 2)) + self.ver_points_arr

            pygame.gfxdraw.filled_polygon(surface, border_points.astype(int), (0, 0, 0))
            pygame.gfxdraw.aapolygon(surface, border_points.astype(int), (0, 0, 0))


        pygame.gfxdraw.filled_polygon(surface, self.ver_points_arr.astype(int), self.color)
        pygame.gfxdraw.aapolygon(surface, self.ver_points_arr.astype(int), self.color)
        # pygame.draw.polygon(surface, self.color, self.ver_points_arr)

        # pygame.draw.circle(surface, RED, (points_tmp[1][0], points_tmp[1][1]), 2)
        # pygame.draw.circle(surface, (247, 122, 59), (points_tmp[0][0], points_tmp[0][1]), 4)

        # pygame.draw.circle(surface, GREEN, (points_tmp[2][0], points_tmp[2][1]), 2)
