from math import isclose, sin, cos, pi
from special_r.BasicRect import BasicRect


class LoopRect(BasicRect):
    def __init__(self, x, y, xp, yp, w, h, r, target_r, color=(0, 55, 255)):
        super().__init__(x, y, xp, yp, w, h, r, color=color)
        self.target_r = target_r

        self.updates_since_state_change = 0

    def update(self, ts):
        super(LoopRect, self).update(ts)
        self.updates_since_state_change += 1
        tmp_s = sin(self.r)
        tmp_c = cos(self.r)
        print(tmp_c, tmp_s)
        if self.pinned:
            target_s = sin(self.target_r)
            target_c = cos(self.target_r)
        else:
            target_s = sin(self.target_r + pi)
            target_c = cos(self.target_r + pi)
        print(tmp_c, tmp_s, target_c, target_s)
        if isclose(target_s, tmp_s, abs_tol=0.1) and \
           isclose(target_c, tmp_c, abs_tol=0.1) and \
           self.updates_since_state_change > 50:
            print("Asddd")
            if self.pinned:
                self.unpin()
            else:
                self.pin()
                self.gravity_dir *= -1.
                self.target_r += pi

            self.updates_since_state_change = 0
