import sys

from special_r.BasicRect import *
from special_r.PinRect import PinRect
from special_r.Scene import Scene


class KeyUnpinScene(Scene):

    def __init__(self):
        super().__init__()
        for i in range(9):
            x = 50. + 85 * i
            y = 450
            xp, yp = x, y - 20
            w, h = 20, 60
            self.objects.append(PinRect(x, y, w, h, xp, yp, i * 20., color=(0, i * 20 % 255, 255)))
        self.unpin_n = 0

    def update_rule(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                self.objects[self.unpin_n].unpin()
                self.unpin_n += 1
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    s = KeyUnpinScene()
    s.animate(0)
