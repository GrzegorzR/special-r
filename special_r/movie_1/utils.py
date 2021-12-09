import itertools

import numpy as np
from colour import Color

from special_r.Scene import Scene
from special_r.examples.state_pym import StatePym


class TranslationScene(Scene):
    def __init__(self, objects, img_size, frames_num, bg_color_1, bg_color_2):
        super().__init__(objects, img_size, bg_color_1)
        self.bg_color_1, self.bg_color_2 = bg_color_1, bg_color_2
        self.frames_num = frames_num
        bg_gradient = [c.hex_l.upper() for c in Color(bg_color_1).range_to(Color(bg_color_2), int(frames_num))]
        self.bg_gradient = itertools.cycle(bg_gradient)

    def update_bg(self, surface):
        surface.fill(next(self.bg_gradient))


class PyramidsScene(Scene):

    def __init__(self, objects_fun, frames_num, dt, bg_color, img_size=(1920, 1080)):
        self.objects_fun = objects_fun
        self.dt = dt

        self.frames_num = int(frames_num)

        objects = objects_fun()
        super().__init__(objects, img_size=img_size, bg_color=bg_color)

    def save_frames(self, output_dir):
        self.animate(dt=self.dt, output_dir=output_dir, fps=60, save_range=(0, self.frames_num))

    def display(self):
        self.animate(dt=self.dt, output_dir=None, fps=60, save_range=(0, self.frames_num))

    def get_initial_states(self):
        self.restart()
        return self.get_current_states()

    def get_end_states(self):
        self.restart()
        for i in range(self.frames_num):
            print(i)
            for o in self.objects:
                o.update(self.dt)
        return self.get_current_states()

    def restart(self):
        self.objects = self.objects_fun()

    def get_current_states(self):
        current_states = []
        for o in self.objects:
            state = {
                'pos': [(o.x, o.y)],
                'xyt': [(o.x_t, o.y_t)],
                'scale': [o.scale],
                'size': [(o.w, o.h)],
                'height': [o.height]
            }
            current_states.append(state)
        return current_states

    def get_color_data(self):
        colorsets = []
        borders_colorsets = []
        for o in self.objects:
            colorsets.append(o.colors)
            borders_colorsets.append(o.borders_colors)

        return colorsets, borders_colorsets, self.bg_col


def get_nearest_corner(img_size, pos, dist=100):
    corners = ((-dist, -dist), (-dist, img_size[1] + dist),
               (img_size[0] + dist, -dist), (img_size[0] + dist, img_size[1] + dist))
    nodes = np.asarray(corners)
    dist_2 = np.sum((nodes - pos) ** 2, axis=1)
    asd = nodes[np.argmin(dist_2)]
    return asd[0], asd[1]


def animate_transition(states_1, states_2, colorsets_1, colorsets_2, borders_colors_1, borders_colors_2,
                       bg_color1, bg_color2, output_dir='out/translation_test', img_size=(1920, 1080)):
    height = 13
    transition_time = 7.5
    dt = 0.05
    frames_per_state = transition_time / dt


    if len(states_1) > len(states_2):
        dif = len(states_1) - len(states_2)
        for i in range(len(states_1) - dif, len(states_1)):
            last_position = states_1[i]['pos']
            nearest_corner = get_nearest_corner(img_size, last_position)
            states_1[i]['pos'].append(nearest_corner)
            states_1[i]['size'].append((150, 150))

    if len(states_1) < len(states_2):
        dif = len(states_2) - len(states_1)
        for i in range(len(states_2) - dif, len(states_2)):
            first_position = states_2[i]['pos'][0]
            nearest_corner = get_nearest_corner(img_size, first_position)
            states_2[i]['pos'] = [nearest_corner, first_position]
            states_2[i]['size'].insert(0, (150, 150))

    output_states = []
    lower_len = min(len(states_1), len(states_2))
    higher_len = max(len(states_1), len(states_2))

    for i in range(lower_len):
        translation_states = {
            'pos': states_1[i]['pos'] + states_2[i]['pos'],
            'xyt': states_1[i]['xyt'] + states_2[i]['xyt'],
            'scale': states_1[i]['scale'] + states_2[i]['scale'],
            'size': states_1[i]['size'] + states_2[i]['size']

        }
        output_states.append(translation_states)

    output_states = output_states + states_1[lower_len:] + states_2[lower_len:]
    colorsets_1_cycle = itertools.cycle(colorsets_1)
    colorsets_2_cycle = itertools.cycle(colorsets_2)
    colorsets_1 = [next(colorsets_1_cycle) for _ in range(higher_len)]
    colorsets_2 = [next(colorsets_2_cycle) for _ in range(higher_len)]
    borders_colors_1_cycle = itertools.cycle(borders_colors_1)
    borders_colors_2_cycle = itertools.cycle(borders_colors_2)
    borders_colors_1 = [next(borders_colors_1_cycle) for _ in range(higher_len)]
    borders_colors_2 = [next(borders_colors_2_cycle) for _ in range(higher_len)]


    pyms = []

    for i in range(higher_len):
        p = StatePym(output_states[i], transition_time, height, colorsets_1[i], borders_colors=borders_colors_1[i])
        p.change_colorset(colorsets_2[i], transition_time=transition_time)
        p.change_borders_colorstes(borders_colors_2[i], transition_time=transition_time)
        pyms.append(p)

    # states_num = len(output_states[0]['pos'])
    frames_num = frames_per_state

    s = TranslationScene(pyms, img_size, frames_num, bg_color_1=bg_color1, bg_color_2=bg_color2)
    s.animate(dt, output_dir, save_range=(0, frames_num))


def make_movie(scenes, out_dir):
    for s in scenes:
        s.restart()

    for i in range(len(scenes) - 1):
        scenes[i].save_frames(out_dir)
        colors_1, borders_colors_1, bg_color_1 = scenes[i].get_color_data()
        colors_2, borders_colors_2, bg_color_2 = scenes[i+1].get_color_data()

        states_init  = scenes[i].get_current_states()
        states_end = scenes[i+1].get_initial_states()
        animate_transition(states_init, states_end, colors_1, colors_2,
                           borders_colors_1, borders_colors_2, bg_color_1, bg_color_2, output_dir=out_dir)

    scenes[-1].save_frames(out_dir)


