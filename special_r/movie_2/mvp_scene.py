from copy import deepcopy
from random import shuffle

import numpy as np
from math import pi, sqrt
from scipy.misc import derivative

from special_r.Scene import Scene
from special_r.movie_2.movie_2_objects import Shape
from special_r.utils.colorsets import blue_crystal_vienna, colorset_little_sad_boy_aka_lsd
from special_r.utils.parametric_functions import create_smooth_transition_fun, concatenate_functions


class ShapesContainer:

    def __init__(self, shapes: list):
        self.shapes = shapes


class Rhombus_60_120(Shape):
    def __init__(self, x, y, s):
        r1 = [(x + s, y),
              (x, y + s * (1 / sqrt(3.))),
              (x - s, y),
              (x, y - s * (1 / sqrt(3.)))]
        ver_points_arr = np.array(r1)
        super().__init__(ver_points_arr)


def get_single_tile(x, y, s, colorset):
    sh = Rhombus_60_120(x, y, s)
    sh.color = colorset[0]

    sh_small = deepcopy(sh)
    sh_small.color = (200, 1, 1)
    sh_small.scale_self(1. / (sqrt(3.) * 2))
    sh_small.translation((s / 2.) * (1 / sqrt(3)), 0)
    shapes = [sh]
    # colorset =
    for i in range(0, 6):
        sh_tmp = deepcopy(sh_small)
        sh_tmp.color = (200, 20 * i + 10, 1)
        sh_tmp.rotate((pi / 3. * i) + pi / 2., (x, y))
        shapes.append(sh_tmp)

    r1_ver_points = np.array([
        shapes[0].ver_points_arr[3],
        shapes[1].ver_points_arr[1],
        shapes[-1].ver_points_arr[0]])

    r2_ver_points = np.array([
        shapes[0].ver_points_arr[3],
        shapes[2].ver_points_arr[1],
        shapes[2].ver_points_arr[0]])

    r3_ver_points = np.array([
        shapes[0].ver_points_arr[1],
        shapes[3].ver_points_arr[3],
        shapes[3].ver_points_arr[0]])

    r4_ver_points = np.array([
        shapes[0].ver_points_arr[1],
        shapes[5].ver_points_arr[1],
        shapes[5].ver_points_arr[0]])
    k1_ver_points = np.array([
        shapes[0].ver_points_arr[2],
        shapes[2].ver_points_arr[0],
        shapes[2].ver_points_arr[3],
        shapes[3].ver_points_arr[0]])

    k2_ver_points = np.array([
        shapes[0].ver_points_arr[0],
        shapes[5].ver_points_arr[0],
        shapes[5].ver_points_arr[3],
        shapes[6].ver_points_arr[0]])

    r1 = Shape(r1_ver_points, color=colorset[1])

    r2 = Shape(r2_ver_points, color=colorset[2])
    r3 = Shape(r3_ver_points, color=colorset[3])
    r4 = Shape(r4_ver_points, color=colorset[2])
    k1 = Shape(k1_ver_points, color=colorset[3])
    k2 = Shape(k2_ver_points, color=colorset[1])

    # k1 = Shape(k1_ver_points, color='#010D26')

    shapes += [r1, r2, r3, r4, k1, k2]
    for s in shapes[1:]:
        s.scale_self(0.66)
    return shapes[1:]


if __name__ == '__main__':
    colors = colorset_little_sad_boy_aka_lsd
    # shuffle(colors)
    # x, y = 400, 400
    s = 300
    shapes = []
    for x in range(5):
        for y in range(5):
            shapes += get_single_tile(x * s * 2, y * s * 2 * (1 / sqrt(3)), s, colors)
    for x in range(5):
        for y in range(5):
            shapes += get_single_tile(x * s * 2 + s, y * s * 2 * (1 / sqrt(3)) + (1 / sqrt(3)) * s, s, colors)


    # shapes += get_single_tile(x+400, y,s)
    # shapes += get_single_tile(x + 200, y-s*(1/sqrt(3)), s)
    class MvpRotScene(Scene):

        def __init__(self, objects, s, bg_color, img_size):
            super().__init__(objects, bg_color=bg_color, img_size=img_size)
            #self.trans_functions = []
            #for i in range(10):
            #    self.trans_functions.append(create_smooth_transition_fun(0, pi, (i * 5) + 1, (i + 1) * 5))

            self.trans_fun_1 = concatenate_functions([create_smooth_transition_fun(0, pi, 0, 5),
                                                      create_smooth_transition_fun(pi, 2*pi, 29, 34)],
                                                     [(0,10), (10,40)])

            self.trans_fun_2 = concatenate_functions([create_smooth_transition_fun(0, pi, 4, 9),
                                                      create_smooth_transition_fun(pi, 2*pi, 25, 30)],
                                                      [(0, 10),(10, 40)])

            self.trans_fun_3 = concatenate_functions([create_smooth_transition_fun(0, pi, 8, 13),
                                                      create_smooth_transition_fun(pi, 2*pi, 21, 26)],
                                                     [(0, 15), (15, 40)])
            self.trans_fun_4 = concatenate_functions([create_smooth_transition_fun(0, pi, 12, 17),
                                                      create_smooth_transition_fun(pi, 2 * pi, 17, 22)],
                                                     [(0, 17), (17, 50)])
            #self.trans_fun_4 =create_smooth_transition_fun(0, 2*pi, 12, 22)
            max_dist = 50
            point = np.array([200, 216])
            for s in self.objects:
                dist = np.linalg.norm(point - s.centroid())
                if dist < max_dist:
                    s.color = '#a132c3'

        def update_rule(self, dt=0.1):
            s = 300
            max_dist = (s / sqrt(3))

            rot_point_1 = np.array([s, 4 * (s / sqrt(3) / 2)])
            rot_point_2 = np.array([s * 1.5, 7 * (s / sqrt(3) / 2)])
            rot_point_3 = np.array([2 * s, 10 * (s / sqrt(3) / 2)])
            rot_point_4 = np.array([2.5 * s, 13 * (s / sqrt(3) / 2)])

            rot_point_5 = np.array([0.5 * s, 1 * (s / sqrt(3) / 2)])

            for s in self.objects:
                dist = np.linalg.norm(rot_point_1 - s.centroid())
                dist2 = np.linalg.norm(rot_point_2 - s.centroid())
                dist3 = np.linalg.norm(rot_point_3 - s.centroid())
                dist4 = np.linalg.norm(rot_point_4 - s.centroid())
                dist5 = np.linalg.norm(rot_point_5 - s.centroid())
                if dist < max_dist:
                    # shapes_to_rotation.append(s)
                    s.rotate(derivative(self.trans_fun_1, self.t) * dt, rot_point_1)
                if dist2 < max_dist:
                    s.rotate(derivative(self.trans_fun_2, self.t) * dt, rot_point_2)
                if dist3 < max_dist:
                    s.rotate(derivative(self.trans_fun_3, self.t) * dt, rot_point_3)
                if dist4 < max_dist:
                    s.rotate(derivative(self.trans_fun_4, self.t) * dt, rot_point_4)
                #if dist5 < max_dist:
                #    s.rotate(derivative(self.trans_fun_4, self.t) * dt, rot_point_5)
            # if self.t >5:


    dt = 0.05
    s = MvpRotScene(shapes, s, bg_color=colors[0], img_size=(s * 4, s * 4))
    s.animate(dt=dt, save_range=(0, 40 / dt), output_dir='out/movie_2/rot_scene')
