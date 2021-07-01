import math
import numpy as np
from special_r.BasicRect import BasicRect


class PinRect(BasicRect):
    def __init__(self, x, y,  w, h, xp=0, yp=0, r=0, vr=0.05, color=(0, 0, 255)):
        super().__init__(x, y,  w, h, xp, yp, r, vr, color)

        self.pinned = True


    def draw(self, surface):
        super(PinRect, self).draw(surface)
        points_tmp = self.piv_points_arr
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

        #pygame.gfxdraw.filled_polygon(surface, self.ver_points_arr, self.color)
        #pygame.gfxdraw.filled_polygon(surface, [[i[0]+1, i[1]+1] for i in self.ver_points_arr], (0, 0, 0,))

    def update_rotation(self, ts):


        if not self.pinned:
            self.xp, self.yp = self.center[0], self.center[1]

        super(PinRect, self).update_rotation(ts)

        if self.pinned:
            self.ar = -math.sin(self.r) * 0.01 * self.gravity_dir

    def unpin(self):
        #points_tmp = self.piv_points_arr
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

if __name__ == '__main__':
    from special_r.Scene import Scene

    x,y = 200., 200.,
    w,h = 100., 50.
    r = PinRect(x,y,w,h,)
    s = Scene([r], 0)
    s.animate(0)

