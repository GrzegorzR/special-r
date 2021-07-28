from special_r.BasicRect import BasicRect


class BorderRect:
    def __init__(self, x, y, w, h, border, xp=0, yp=0, r=0., vr=0.1, color=(0, 0, 255), border_color=(0, 0, 0)):
        self.main_rect = BasicRect(x, y, w - border, h - border, xp=xp, yp=yp, r=r, vr=vr, color=color)
        self.border = BasicRect(x, y, w, h, xp=xp, yp=yp, r=r, vr=vr, color=border_color)

    def update(self, ts):
        self.main_rect.update(ts)
        self.border.update(ts)

    def draw(self, surface):
        self.border.draw(surface)
        self.main_rect.draw(surface)
