import itertools
from math import sin, pi

from special_r.Scene import Scene
from special_r.pyramid.Pyramid import PyramidMoving
from special_r.utils.colorsets import vienna_wom, white_to_green

states = {
    'pos': [],
    'xyt': [],
    'scale': [],
    'size': []
}


class StatePym(PyramidMoving):
    def __init__(self,  states, transition_time, height, colors, borders_colors=None):
        self.states_pos = itertools.cycle(states['pos'])
        self.states_xyt = itertools.cycle(states['xyt'])
        self.states_scale = itertools.cycle(states['scale'])
        self.states_size = itertools.cycle(states['size'])

        self.transition_time = transition_time
        self.current_state = 0.5
        # x, y, w, h, move_fun, colors,
        xt0, yt0 = next(self.states_xyt)
        x0, y0 = next(self.states_pos)
        w0, h0 = next(self.states_size)
        scale0 = next(self.states_scale)
        move_fun = lambda t: (xt0, yt0)

        super().__init__(x0, y0, w0, h0, move_fun, height=height, scale=scale0,
                         colors=colors, borders_colors=borders_colors)

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
        asd = next(self.states_pos)
        x1, y1 = asd

        xt1, yt1 = next(self.states_xyt)
        s1 = next(self.states_scale)
        w1, h1 = next(self.states_size)

        self.change_pos(x1, y1, self.transition_time)
        self.change_size(h1, w1, self.transition_time)
        self.change_xyt(xt1, yt1, self.transition_time)
        self.change_scale(s1, self.transition_time)


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
    # colors = white_to_green(height + 1)
    transition_time = 7.
    states = {'xyt': [(0.2, 0.2), (0.2, 0.2), (0.2, -0.2), (-0.2, -0.2), (0., 0.)],
              'pos': [(x, y), (x, y - 200), (x, y), (x, y), (x, y)],
              'scale': [scale, scale, scale, scale, scale],
              'size': [(w, h), (w, h), (w, h), (w, h), (w, h)]
              }
    p = StatePym(states, transition_time, height, colors)

    pyramides = []
    pyramides.append(p)
    s = Scene([p], bg_color=colors[0])
    s.animate(dt, output_dir=out_dir, save_range=(0, steps))


if __name__ == '__main__':
    scene_states()
