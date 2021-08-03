import itertools
from math import sin, pi

from special_r.Scene import Scene
from special_r.pyramid.Pyramid import PyramidMoving
from special_r.utils.colorsets import vienna_wom, white_to_green


class StatePym(PyramidMoving):
    def __init__(self, x, y, w, h, states_list, transition_time, height, scale, colors):
        self.states_list = itertools.cycle(states_list)
        self.transition_time = transition_time
        self.current_state = 0
        # x, y, w, h, move_fun, colors,
        move_fun = lambda t: (0., 0.)
        super().__init__(x, y, w, h, move_fun, height=height, scale=scale, colors=colors)

    def update(self, ts):
        new_state = self.calculate_state()
        if not new_state == self.current_state:
            self.change_state()
            self.current_state = new_state

        super().update(ts)

    def calculate_state(self):
        if sin((self.t * pi) / self.transition_time) >= 0:
            return 1
        else:
            return 0

    def change_state(self):
        x1, y1 = next(self.states_list)
        self.change_xyt(x1, y1, self.transition_time)


def scene_states():
    out_dir = 'out/pym_18'
    out_dir = None
    colors = vienna_wom

    w, h = 200, 200
    height = 15
    dt = 0.05
    scale = 0.93
    steps = (7. / dt) * 5 * 2
    x = 400
    y = 400
    colors = white_to_green(height + 1)
    transition_time = 7.
    states = [(0.2, 0.2), (-0.2, 0.2), (0.2, -0.2),
              (-0.2, -0.2), (0., 0.)]
    p = StatePym(x, y, w, h, states, transition_time, height, scale, colors[1:])

    pyramides = []
    pyramides.append(p)
    s = Scene([p], bg_color=colors[0])
    s.animate(dt, output_dir=out_dir, save_range=(0, steps))


if __name__ == '__main__':
    scene_states()
