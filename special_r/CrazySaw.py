import sys
from math import pi, sin, cos
from pygame.locals import *

from special_r.Rect import *
from special_r.Rect import Rect

from special_r.utils.colorsets import basic_custom_mechanical_keybors_gone_wrong as colorset


class CrazySaw(Rect):
    def __init__(self, x, y, w, h, r, ax, v_val, color=(255,0,0)):
        super().__init__(x, y, x, y, w, h, r, color)
        self.p0 = np.array([x, y])
        self.x0, self.y0 = x, y
        # self.x_range = x_range
        # self.y_range = y_range
        self.k = 0.01
        ax = np.array(ax)
        self.axis = ax / np.linalg.norm(ax)
        self.v = self.axis * v_val

    def update_position(self, ts):
        dist = self.p0 - self.center
        self.a = self.k * dist  # * self.axis

        self.v = self.v + (self.a * float(ts))

        ds = self.v * ts
        self.center += ds
        #print(self.a)
        # self.update_postions_arrays()

        self.ver_points_arr += ds
        self.piv_points_arr += ds

    def update_rotation(self, ts):
        # self.vr += self.ar * ts
        # self.vr *= self.rotation_fraction
        dist = abs(self.a[0])
        self.vr = dist * 0.1 + 0.5
        self.color = (93 , 183-int(self.vr * 100)*2, 222-int(self.vr * 100)*2)
        #self.color = (int(self.vr * 100), 50, 150)
        #print(self.color)
        dr = round(self.vr * ts, 5)
        # self.r += dr
        # self.points_to_print.append([self.piv_points_arr[0][0], self.piv_points_arr[0][1]])
        # if not self.pinned:
        self.xp, self.yp = self.center[0], self.center[1]

        rot_matrix = self.get_rotation_matrix(dr)

        points_tmp = np.pad(self.ver_points_arr, ((0, 0), (0, 1)), constant_values=1)
        self.ver_points_arr = np.dot(rot_matrix, points_tmp.T)[:2, :].T

    def update(self, ts):
        ts = float(ts)
        # print(self.v)
        self.update_rotation(ts)
        self.update_position(ts)



if __name__ == '__main__':
    pygame.init()

    FPS = 25.

    clock = pygame.time.Clock()
    img_size = 566
    DISPLAYSURF = pygame.display.set_mode((img_size, img_size))

    rs = []
    x, y = img_size/2, img_size/2
    xp, yp = x, y

    #se

    for i in np.arange(0, 2. * pi, pi / 8):
        ax_x = sin(i)
        ax_y = cos(i)
        rs.append(CrazySaw(x, y, 20. , 60. , i , [ax_x, ax_y], 20))

    c, unpin_n = 1, 0
    while c<=106:
        # print(c, r.vr, math.sin(r.r), math.cos(r.r), r.r)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(colorset['background'])
        for r in rs:
            r.update(0.3)
            r.draw(DISPLAYSURF)
        pygame.display.update()
        c += 1
        pygame.image.save(DISPLAYSURF, "gif_1/{}.png".format(str(c).zfill(4)))

        clock.tick(FPS)
