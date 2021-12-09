from math import pi

from special_r.examples.state_pym import StatePym
from special_r.movie_1.utils import PyramidsScene
from special_r.pyramid.Pyramid import PyramidMoving
from special_r.utils.colorsets import *
from special_r.utils.parametric_functions import ParametricCircle, LissajousCurve

c = chinskie

xyts_dict = {
    'new': [
        [(0., 0.), (-0.4, 0.4), ],
        [(0., 0.), (-0.4, -0.4), ],
        [(0., 0.), (0.4, 0.4), ],
        [(0., 0.), (0.4, -0.4), ],
    ]
    ,
    'old': [

        [(-0.4, 0.4), (-0.4, 0.4), (0, 0)],
        [(-0.4, -0.4), (-0.4, -0.4), (0, 0)],
        [(0.4, 0.4), (0.4, 0.4), (0, 0)],
        [(0.4, -0.4), (0.4, -0.4), (0, 0)],
    ],
    'first': [
        [(0., 0.), (-0.4, 0), (-0.4, 0.4), (0, 0.4), (0., 0.)],
        [(0., 0.), (-0.4, 0), (-0.4, -0.4), (0, -0.4), (0., 0.)],
        [(0., 0.), (0.4, 0), (0.4, 0.4), (0, 0.4), (0., 0.)],
        [(0., 0.), (0.4, 0), (0.4, -0.4), (0, -0.4), (0., 0.)],
    ]

}


def get_scen3_pyms_chuck(x, y, size, xyt_type):
    w, h = 200. / size, 200. / size
    scale = 0.85
    ofset = 100 / size
    poses = [(x - ofset, y + ofset), (x - ofset, y - ofset), (x + ofset, y + ofset,), (x + ofset, y - ofset), ]
    xyts = xyts_dict[xyt_type]

    pyms = []
    for i in range(len(poses)):
        states = {'xyt': xyts[i],
                  'pos': [poses[i] for _ in range(5)],
                  'scale': [scale, scale, scale, scale, scale],
                  'size': [(w, h), (w, h), (w, h), (w, h), (w, h)]
                  }
        p = StatePym(states, 5, 13, c, borders_colors=c)
        pyms.append(p)
    return pyms




def get_pyms_scene_3():
    return get_scen3_pyms_chuck(1920 / 2, 1080 / 2, 1, 'first')


def get_pyms_scene_3_2():
    pyms = get_scen3_pyms_chuck(1920 / 2, 1080 / 2, 1, 'old')
    pyms += get_scen3_pyms_chuck(1920 / 2, 1080 / 8, 2, 'new')
    pyms += get_scen3_pyms_chuck(1920 / 2, 1080 *(7/8) , 2, 'new')
    pyms += get_scen3_pyms_chuck(1920 / 4, 1080 / 2, 2, 'new')
    pyms += get_scen3_pyms_chuck(1920 * (3 / 4), 1080 / 2, 2, 'new')
    return pyms

def get_pyms_scene_3_3():
    pyms = get_scen3_pyms_chuck(1920 / 2, 1080 / 2, 1, 'old')
    pyms += get_scen3_pyms_chuck(1920 / 2, 1080 / 8, 2, 'old')
    pyms += get_scen3_pyms_chuck(1920 / 2, 1080 *(7/8) , 2, 'old')
    pyms += get_scen3_pyms_chuck(1920 / 4, 1080 / 2, 2, 'old')
    pyms += get_scen3_pyms_chuck(1920 * (3 / 4), 1080 / 2, 2, 'old')

    x,y = 1920 , 1080
    pyms += get_scen3_pyms_chuck(x/4, y/4, 3,'new')
    pyms += get_scen3_pyms_chuck(x *(3/4), y / 4, 3, 'new')

    pyms += get_scen3_pyms_chuck(x/4, y*(3/4), 3,'new')
    pyms += get_scen3_pyms_chuck(x *(3/4), y *(3/4), 3, 'new')

    pyms += get_scen3_pyms_chuck(x /8, y /2, 3, 'new')
    pyms += get_scen3_pyms_chuck(x *(7/8), y / 2, 3, 'new')

    pyms += get_scen3_pyms_chuck(x * (3/8), y , 3, 'new')
    pyms += get_scen3_pyms_chuck(x * (3 / 8), 0, 3, 'new')

    pyms += get_scen3_pyms_chuck(x * (5/8), y , 3, 'new')
    pyms += get_scen3_pyms_chuck(x * (5 / 8), 0, 3, 'new')
    #pyms += get_scen3_pyms_chuck(x / 2, y *(7/8) , 3, 'new')
    #pyms += get_scen3_pyms_chuck(x / 4, y / 2, 3, 'new')
    #pyms += get_scen3_pyms_chuck(x * (3 / 4), y / 2, 3, 'new')



    return pyms

def get_scene_3_obj():
    bg_color = c[1]
    dt = 0.05
    return PyramidsScene(get_pyms_scene_3, 100 * 4, dt, bg_color, img_size=(1920, 1080))


def get_scene_3_2_obj():
    bg_color = c[1]
    dt = 0.05
    return PyramidsScene(get_pyms_scene_3_2, 100 * 2, dt, bg_color, img_size=(1920, 1080))

def get_scene_3_3_obj():
    bg_color = c[1]
    dt = 0.05
    return PyramidsScene(get_pyms_scene_3_3, 100 * 2, dt, bg_color, img_size=(1920, 1080))

if __name__ == '__main__':
    s = get_scene_3_3_obj()
    s.display()
