import shutil

import numpy as np
from colour import Color

from special_r.Scene import Scene
from special_r.examples.state_pym import StatePym
from special_r.movie_1.utils import PyramidsScene, get_nearest_corner
from special_r.utils.colorsets import vienna_wom, colors_range_hex

END_STEPS = 6
ALL_STEPS = 9
IMG_SIZE = (1920, 1080)


def get_colorset(n):
    cream = '#D5CCBA'
    cream = '#FFFFFF'
    blue = '#A9BBC6'
    light_red = '#c4ab9a'
    red = '#8C0303'
    black = '#121717'
    dark_red = '#380200'

    def colors_list(c1, c2):
        return [c1 for _ in range(n - 1)] + [c2]

    colorsets = [colors_list(cream, light_red),
                 colors_list(cream, red),
                 colors_list(cream, light_red),
                 colors_list(cream, blue),
                 colors_list(black, cream),
                 colors_list(cream, dark_red),

                 colors_list(cream, red),
                 colors_list(black, cream),
                 colors_list(cream, dark_red),  #
                 colors_list(cream, red),

                 colors_list(cream, dark_red),
                 colors_list(cream, blue),
                 colors_list(cream, light_red),
                 colors_list(black, cream),
                 colors_list(cream, dark_red),
                 colors_list(cream, blue),

                 colors_list(black, cream),
                 colors_list(cream, red),
                 colors_list(cream, blue),
                 colors_list(cream, light_red)
                 ]
    return colorsets


def get_positions():
    positions = [[(100, -105), (100, 100)],
                 [(300, -105), (300, 100)],
                 [(500, -105), (500, 100)],
                 [(700, -105), (700, 100)],
                 [(900, -105), (900, 100)],
                 [(-100, -100), (1100, 200)],

                 [(-100, -100), (100, 300)],
                 [(-100, -100), (300, 300)],
                 [(600, 300), (600, 300)],  #
                 [(-100, -100), (900, 300)],

                 [(-100, -100), (100, 500)],
                 [(-100, -100), (300, 600)],
                 [(-100, -100), (500, 500)],
                 [(-100, -100), (700, 500)],
                 [(-100, -100), (900, 500)],
                 [(-100, -100), (1100, 500)],

                 [(-100, -100), (100, 700)],
                 [(-100, -100), (500, 700)],
                 [(-100, -100), (700, 700)],
                 [(-100, -100), (1000, 700)]
                 ]
    pos = [[get_nearest_corner(IMG_SIZE, n[1], dist=160), n[1]] for n in positions]
    pos[8] = [(650, 550), (600, 300), (600, 300)]
    pos = [[p[0], (p[1][0] + 360, p[1][1] + 140), (p[1][0] + 360, p[1][1] + 140)] for p in pos]
    for i, p in enumerate(pos):
        pos[i] = p + [p[-1] for _ in range(END_STEPS)]

    return pos


def get_xyt():
    right_down, left_down, left_up, right_up = (0.025, 0.025), (-0.025, 0.025), (-0.025, -0.025), (0.025, -0.025)

    xyt = [right_up, right_up, left_down, right_down, right_down, (0, 0),
           right_down, left_down, (0, 0), left_down,
           left_down, (0, 0), left_down, left_up, right_up, left_up,
           right_up, left_up, right_up, (0, 0)]

    xyt = [[(0, 0), (0, 0), p] for p in xyt]
    xyt[8] = [(0.15, 0.1), (0, 0), (0, 0)]

    def add_next_positions(positions):
        last_position = positions[-1]
        if last_position == right_down:
            next_position = left_down
        elif last_position == left_down:
            next_position = left_up
        elif last_position == left_up:
            next_position = right_up
        elif last_position == right_up:
            next_position = right_down
        else:
            next_position = (0, 0)
        positions.append(next_position)

    for i in range(END_STEPS):
        for p in xyt:
            add_next_positions(p)

    return xyt


def get_sizes():
    small = (195, 195)
    big_vertical = (195, 395)
    big_horizontal = (395, 195)

    sizes = [small, small, small, small, small, big_vertical,
             small, small, big_horizontal, small,
             small, big_vertical, small, small, small, small,
             small, small, small, big_horizontal]
    sizes = [[s] for s in sizes]
    sizes[8] = [(400, 400), big_horizontal, big_horizontal, big_horizontal, big_horizontal]
    for i, s in enumerate(sizes):
        sizes[i] = s + [s[-1] for _ in range(END_STEPS + 2)]
    return sizes


def get_borders_colors(n):
    grey = '#EBE6E6'
    black = '#121717'
    cream = '#FFFFFF'
    grey_to_black = colors_range_hex(Color(black), Color(grey), n)
    all_black = [black for _ in range(n)]
    last_black = [black] + [cream for _ in range(n - 2)] + [black]

    colors = [grey_to_black, last_black, grey_to_black, grey_to_black, all_black, grey_to_black,
              grey_to_black, all_black, grey_to_black, last_black,
              last_black, grey_to_black, grey_to_black, all_black, grey_to_black, grey_to_black,
              all_black, grey_to_black, last_black, grey_to_black]
    return colors


def get_states_list(scale=0.92):
    positions = get_positions()
    xyt_arr = get_xyt()
    sizes = get_sizes()

    states_list = []
    for i in range(len(positions)):
        states = {
            'pos': positions[i],
            'xyt': xyt_arr[i],
            'scale': [scale for _ in range(ALL_STEPS)],
            'size': sizes[i]
        }
        states_list.append(states)

    return states_list


def get_final_states():
    states = get_states_list()
    final_states = []
    for i in range(len(states)):
        final_states.append(
            {
                'pos': [states[i]['pos'][-1]],
                'xyt': [states[i]['xyt'][-1]],
                'scale': [states[i]['scale'][-1]],
                'size': [states[i]['size'][-1]]
            }
        )
    return final_states


def scene_1():
    img_size = (1920, 1080)
    height = 13
    transition_time = 5.
    dt = 0.05
    frames_per_state = transition_time / dt
    scale = 0.92

    colorsets = get_colorset(height)
    borders_colors = get_borders_colors(height)
    pyms = []

    states = get_states_list()
    states_num = len(states[0]['pos'])
    frames_num = states_num * frames_per_state

    for i in range(len(colorsets)):
        p = StatePym(states[i], transition_time, height, colorsets[i], borders_colors=borders_colors[i])
        pyms.append(p)

    s = Scene(pyms, img_size, bg_color='#82808A')
    s.animate(0.05, 'out/move1/scene_1_1', save_range=(0, frames_num))
    return states


def get_pyms_scene_1():
    height = 13
    transition_time = 5.
    colorsets = get_colorset(height)
    borders_colors = get_borders_colors(height)
    pyms = []

    states = get_states_list()

    for i in range(len(colorsets)):
        p = StatePym(states[i], transition_time, height, colorsets[i], borders_colors=borders_colors[i])
        pyms.append(p)
    return pyms


def get_scene_1_obj():
    bg_color = '#82808A'
    img_size = (1920, 1080)
    transition_time = 5.
    dt = 0.05
    frames_per_state = transition_time / dt

    states = get_states_list()
    states_num = len(states[0]['pos'])
    frames_num = (states_num - 4) * frames_per_state

    return PyramidsScene(get_pyms_scene_1, frames_num, dt, bg_color, img_size)


if __name__ == '__main__':
    out_dir = 'out/move1/scene1_test'
    shutil.rmtree(out_dir)

    s = get_scene_1_obj()
    s.save_frames(out_dir)
