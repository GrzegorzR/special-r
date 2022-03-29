import copy
import math
from math import pi

import numpy as np
import pygame
import pygame.gfxdraw

from special_r.Scene import Scene
from special_r.movie_2.movie_2_fun import line_intersection
from special_r.utils.parametric_functions import create_transition_fun, create_linear_transition_fun
from special_r.utils.callable_objects import CallableNumerical as CN

class Shape:
    def __init__(self, ver_points_arr, color=(100, 150, 150)):
        self.ver_points_arr = ver_points_arr

        self.color = color

    def update(self, ts):
        ts = float(ts)

    def centroid(self):
        xy = np.average(self.ver_points_arr, axis=0)
        return xy

    def rotate(self, angle, p):
        r00, r01, r10, r11 = math.cos(angle), math.sin(angle), -math.sin(angle), math.cos(angle)
        rot_matrix = np.array([[r00, r01, p[0] - (r00 * p[0]) - (r01 * p[1])],
                               [r10, r11, p[1] - (r10 * p[0]) - (r11 * p[1])],
                               [0, 0, 1]])

        points_tmp = np.pad(self.ver_points_arr, ((0, 0), (0, 1)), constant_values=1)
        self.ver_points_arr = np.dot(rot_matrix, points_tmp.T)[:2, :].T

    def rotate_self(self, angle):
        self.rotate(angle, self.centroid())

    def translation(self, dx, dy):
        # print(self.ver_points_arr)
        self.ver_points_arr += np.array([dx, dy])
        # pri

    def scale(self, xs, ys, x, y):
        self.translation(-x, -y)
        scale_mat = np.array([[1, 0, 0],
                              [0, float(ys), 0],
                              [0, 0, 1]])
        points_tmp = np.pad(self.ver_points_arr, ((0, 0), (0, 1)), constant_values=1)
        self.ver_points_arr = np.dot(scale_mat, points_tmp.T)[:2, :].T
        scale_mat = np.array([[float(xs), 0, 0],
                              [0, 1, 0],
                              [0, 0, 1]])
        points_tmp = np.pad(self.ver_points_arr, ((0, 0), (0, 1)), constant_values=1)
        self.ver_points_arr = np.dot(scale_mat, points_tmp.T)[:2, :].T
        self.translation(x, y)

    def scale_self(self, s):
        xy = self.centroid()
        self.scale(s, s, xy[0], xy[1])

    def max_size(self):

        max_x, min_x = np.max(self.ver_points_arr[:, 0]), np.min(self.ver_points_arr[:, 0])
        max_y, min_y = np.max(self.ver_points_arr[:, 1]), np.min(self.ver_points_arr[:, 1])
        return (max_x - min_x) * (max_y - min_y)

    def draw(self, surface):
        if self.color is not None:
            self.ver_points_arr = self.ver_points_arr.astype(float)
            if self.max_size() > 50:
                pygame.gfxdraw.filled_polygon(surface, self.ver_points_arr.astype(int), pygame.Color(self.color))
                pygame.gfxdraw.aapolygon(surface, self.ver_points_arr.astype(int), pygame.Color(self.color))


class ShapeB:

    def __init__(self, shape, border_ratio, border_color):
        self.b_shape = copy.deepcopy(shape)
        self.b_shape.color = border_color
        self.shape = shape
        self.shape.scale_self(border_ratio)

    def draw(self, surface):
        self.b_shape.draw(surface)
        self.shape.draw(surface)

    def update(self, ts):
        pass


class Rhombus(Shape):
    def __init__(self, x, y, p, q, color):
        self.x, self.y = x, y
        self.p, self.q = p, q
        ver_points_arr = np.array([(x, y + (p / 2.)), (x + (q / 2.), y), (x, y - (p / 2.)), (x - (q / 2.), y)])
        super().__init__(ver_points_arr, color)


class Triangle(Shape):
    def __init__(self, a, b, c, color=(150, 150, 100)):
        super().__init__(np.array([a, b, c]), color)


class RhombusFractal:
    def __init__(self, x, y, p_fun, q_fun, colorset, debug=False):

        self.x, self.y = x, y
        self.p_fun, self.q_fun = p_fun, q_fun
        self.p, self.q = p_fun(0.), q_fun(0.)
        self.t = 0
        self.colorset = colorset
        # self.colorset[1]=None
        # print(self.alpha)
        self.scale_time_fun = None
        self.scale_size_fun = None
        self.translations_fun = None
        self.debug = debug

        self.objects = []

    def get_objects_down(self):
        p, q = self.p, self.q
        small_q = p / 2.
        small_p = (p * p) / (2. * q)
        x_1, y_1 = self.x, self.y + p / 4.
        x_2, y_2 = self.x, self.y - p / 4.
        x_3, y_3 = self.x + p / 4., self.y
        x_4, y_4 = self.x - p / 4., self.y

        r_1 = HorRhombusFractal(x_1, y_1, CN(small_p), CN(small_q), self.colorset)
        r_2 = HorRhombusFractal(x_2, y_2, CN(small_p), CN(small_q), self.colorset)
        r_3 = RhombusFractal(x_3, y_3, CN(small_p), CN(small_q), self.colorset)
        r_4 = RhombusFractal(x_4, y_4, CN(small_p), CN(small_q), self.colorset)

        return [r_1, r_2, r_3, r_4]



    def size(self):
        points = [o.ver_points_arr for o in self.objects]
        points = np.concatenate(points)
        # points = np.array(points)
        # print(points)
        max_val = np.max(points, axis=0)
        min_val = np.min(points, axis=0)
        size = (max_val[0] - min_val[0]) * (max_val[1] - min_val[1])
        return size

    def center(self):
        points = [o.ver_points_arr for o in self.objects]
        points = np.concatenate(points)
        # points = np.array(points)
        # print(points)
        max_val = np.max(points, axis=0)
        min_val = np.min(points, axis=0)
        x_center = (max_val[0] + min_val[0]) / 2.
        y_center = (max_val[1] + min_val[1]) / 2.
        return x_center, y_center

    def rotate_self(self, angle):
        x, y = self.center()

        for o in self.objects:
            o.rotate(angle, (x, y))

    def update(self, ts):
        ts = float(ts)
        self.t += ts
        self.p = self.p_fun(self.t)
        self.q = self.q_fun(self.t)

        self.update_objects()
        # if self.scale_fun:
        #    self.scale_self(self.scale_fun(self.t))


    def scale_self(self, v):
        for o in self.objects:
            o.scale_self(v)
    def scale_time(self):
        if self.scale_time_fun:
            s_v, s_p = self.scale_time_fun(self.t)
            if s_p is None:
                s_p = self.center()
            for o in self.objects:
                o.scale(s_v, s_v, s_p[0], s_p[1])

    def update_objects(self):
        self.objects = []
        if self.debug:
            x, y, p, q = self.x, self.y, self.p, self.q
            self.objects.append(Rhombus(x, y, p, q, self.colorset[2]))
        else:
            self.update_rhombuses()
            self.update_trapezoides()
            self.update_triangles()

        # print(asd)
        if self.translations_fun:
            dx, dy = self.translations_fun(self.t)
            for o in self.objects:
                o.translation(dx, dy)
        self.scale_time()

        # print(self.size(), scale_v)
        if self.scale_size_fun:
            scale_v = self.scale_size_fun(self.size())
            # s_v, s_p = self.scale_fun(self.t)
            for o in self.objects:
                o.scale_self(scale_v)

        # self.objects.append(Triangle((x, y), self.objects[3].ver_points_arr[1], self.objects[4].ver_points_arr[2]))

    def update_rhombuses(self):
        x, y, p, q = self.x, self.y, self.p, self.q

        # main rhombus
        self.objects.append(Rhombus(x, y, p, q, self.colorset[4]))
        # small rhombuses
        self.objects.append(Rhombus(x - (p / 4.), y, (p / 2.) * (p / q), p / 2., self.colorset[1]))
        self.objects.append(Rhombus(x, y + (p / 4.), p / 2., (p / 2.) * (p / q), self.colorset[1]))
        self.objects.append(Rhombus(x, y - (p / 4.), p / 2., (p / 2.) * (p / q), self.colorset[1]))
        self.objects.append(Rhombus(x + (p / 4.), y, (p / 2.) * (p / q), p / 2, self.colorset[1]))

    def update_trapezoides(self):
        x, y, p, q = self.x, self.y, self.p, self.q
        A, B, C, D = tuple(self.objects[0].ver_points_arr)
        line_1 = ((x, y), (self.objects[3].ver_points_arr[1] + self.objects[4].ver_points_arr[2]) / 2)
        line_2 = ((x, y), (self.objects[2].ver_points_arr[1] + self.objects[4].ver_points_arr[0]) / 2)
        line_AB = (A, B)
        line_CB = (C, B)
        line_DA = (D, A)
        line_DC = (D, C)

        x_t1, y_t1 = line_intersection(line_1, line_CB)
        x_t2, y_t2 = line_intersection(line_1, line_DA)
        x_t3, y_t3 = line_intersection(line_2, line_AB)
        x_t4, y_t4 = line_intersection(line_2, line_DC)


        # for smaller sizes
        #x_t1, y_t1 = x_t1 + 1, y_t1 - 1
        #x_t2, y_t2 = x_t2 - 1, y_t2 + 1
        #x_t3, y_t3 = x_t3 + 1, y_t3 - 1
        #x_t4, y_t4 = x_t4 - 1, y_t4 + 1

        trapezoid_1 = np.array([[x, y], self.objects[3].ver_points_arr[1], [x_t1, y_t1],
                                self.objects[4].ver_points_arr[2]])

        trapezoid_2 = np.array([[x, y], self.objects[1].ver_points_arr[0], [x_t2, y_t2],
                                self.objects[2].ver_points_arr[3]])

        trapezoid_3 = np.array([[x, y], self.objects[2].ver_points_arr[1], [x_t3, y_t3],
                                self.objects[4].ver_points_arr[0]])
        trapezoid_4 = np.array([[x, y], self.objects[3].ver_points_arr[3], [x_t4, y_t4],
                                self.objects[1].ver_points_arr[2]])

        self.objects.append(Shape(trapezoid_3))
        self.objects.append(Shape(trapezoid_4))
        self.objects.append(Shape(trapezoid_1))
        self.objects.append(Shape(trapezoid_2))

    def update_triangles(self):

        t1 = Triangle(self.objects[0].ver_points_arr[3],
                      self.objects[6].ver_points_arr[2],
                      self.objects[1].ver_points_arr[2],
                      color=self.colorset[2])

        t2 = Triangle(self.objects[0].ver_points_arr[3],
                      self.objects[8].ver_points_arr[2],
                      self.objects[1].ver_points_arr[0],
                      color=self.colorset[2])
        t3 = Triangle(self.objects[0].ver_points_arr[1],
                      self.objects[5].ver_points_arr[2],
                      self.objects[5].ver_points_arr[3],
                      color=self.colorset[2])
        t4 = Triangle(self.objects[0].ver_points_arr[1],
                      self.objects[7].ver_points_arr[2],
                      self.objects[7].ver_points_arr[3],
                      color=self.colorset[2])

        self.objects += [t1, t2, t3, t4]

    def draw(self, surface):
        for o in self.objects:
            o.draw(surface)

    def scale_f_size(self, size):
        return


class HorRhombusFractal(RhombusFractal):

    def __init__(self, x, y, p_fun, q_fun, colorset):
        super().__init__(x, y, p_fun, q_fun, colorset)

    def update(self, ts):
        super().update(ts)
        self.rotate_self(pi / 2.)

    def draw(self, surface):
        super().draw(surface)
