import os
import random
import numpy as np
import drawSvg as draw

from special_r.svg.Element import Element
from special_r.svg.Transformation import Translation, RoseTrans, Scale

W, H = 1080, 1920


def bezier_from_array(a):
    result_svg = draw.Path(transform='', stroke_width=4, stroke='#ffe957', fill='none', id='line_svg')
    d = "M {},{} C {},{} {},{} {},{}".format(*a)
    result_svg.args['d'] = d
    return result_svg


def random_bezier():
    a = np.random.rand(8)*100
    return bezier_from_array(a)


def beziers_line(a1, a2, size=10):

    a_gradient = np.linspace(a1, a2, num=size)
    results = []
    for a in a_gradient:
        results.append(bezier_from_array(a))

    return results

def beziers_random_line(size=10):

    a1 = np.random.rand(8)*100
    a2 = np.random.rand(8)*100
    return beziers_line(a1, a2, size)


def beziers_grid(size=10):
    grad_1 = np.linspace(np.random.rand(8)*100, np.random.rand(8)*100, num=size)
    grad_2 = np.linspace(np.random.rand(8)*100, np.random.rand(8)*100, num=size)

    result = []
    for i in range(size):
        grads = np.linspace(grad_1[i], grad_2[i], num=size)
        result.append([bezier_from_array(g) for g in grads])

    return result

def beziers_random_grid():
    pass


def beziers_cubic():
    pass

def draw_single():
    svg_elem = random_bezier()
    sur = draw.Drawing(W, H, origin='center', displayInline=False)

    sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))
    sur.append(svg_elem)
    sur.savePng('out/bezier/test12aa.png')
    sur.saveSvg('out/bezier/test12aa.svg')

def draw_line():
    svg_array= beziers_random_line()
    positions = np.linspace(-300, 300, num=10)

    sur = draw.Drawing(W, H, origin='center', displayInline=False)
    sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))
    for i, svg_elem in enumerate(svg_array):
        elem = Translation(positions[i], 0)(Element(svg_elem))
        elem.draw(sur)
        #sur.append(svg_elem)
    sur.savePng('out/bezier/test12aa.png')
    sur.saveSvg('out/bezier/test12aa.svg')

def draw_grid(out_dir, curvs=None, filename=None):
    os.makedirs(out_dir, exist_ok=True)
    if not filename:
        filename = "grid_{}".format(len(os.listdir(out_dir)))

    if not curvs:
        curvs = beziers_grid()
    positions = np.linspace(-300, 300, num=10)-50


    sur = draw.Drawing(W, H, origin='center', displayInline=False)
    sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))

    for x in range(10):
        for y in range(10):
            svg_elem = curvs[x][y]

            elem = RoseTrans(12, 50,50)(Element(svg_elem))
            elem = Translation(positions[x], positions[y])(elem)
            elem.draw(sur)

    sur.savePng(os.path.join(out_dir, filename +'.png'))
    sur.saveSvg(os.path.join(out_dir, filename +'.svg'))



def single_bezier_anim(out_dir):
    os.makedirs(out_dir,exist_ok=True)
    size =120
    grad_1 = np.linspace(np.random.rand(8) * 100, np.random.rand(8) * 100, num=size)
    for i, g in enumerate(grad_1):
        filename = "{:03d}".format(i)
        sur = draw.Drawing(W, H, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))
        e = random_bezier(g)
        elem = RoseTrans(6, 10, 10)(Element(e))
        #elem = Translation(-100, -100)(elem)
        elem.draw(sur)
        sur.savePng(os.path.join(out_dir, filename + '.png'))


def animate_line(out_dir, size=10, steps=100, stop_points=1):
    size_modifier = 2.2
    os.makedirs(out_dir,exist_ok=True)

    grad_1 = np.linspace(np.random.rand(8) * 100*size_modifier, np.random.rand(8) * 100*size_modifier, num=steps)
    grad_2 = np.linspace(np.random.rand(8) * 100*size_modifier, np.random.rand(8) * 100*size_modifier, num=steps)

    for i in range(stop_points-1):
        grad_1 = np.append(grad_1,np.linspace(grad_1[-1], np.random.rand(8) * 100*size_modifier, num=steps), axis=0)
        grad_2 = np.append(grad_2, np.linspace(grad_2[-1], np.random.rand(8) * 100*size_modifier, num=steps), axis=0)

    grad_1 = np.append(grad_1, np.linspace(grad_1[-1], grad_1[0], num=steps), axis=0)
    #grad_2 = np.append(grad_2, np.linspace(grad_2[-1], grad_2[0], num=steps), axis=0)
    grad_2 = np.roll(grad_1, 1, axis=0)
    positions = np.linspace(-600, 600, num=size)-150


    for i in range(steps*(stop_points+1)):

        filename = "{:04d}".format(i)
        print(filename)
        sur = draw.Drawing(W, H, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill='#A9BBC6'))
        line = beziers_line(grad_1[i], grad_2[i], size=size)
        for y, svg_elem in enumerate(line):
            elem = RoseTrans(3*(y+2), 100, 100)(Element(svg_elem))
            elem = Scale(1.5)(elem)
            elem = Translation(-150, positions[y])(elem)
            elem.draw(sur)
            sur.savePng(os.path.join(out_dir, filename + '.png'))

if __name__ == '__main__':
    #for i in range(100):
    #    draw_grid('out/bezier/grid_rose')

    #single_bezier_anim('out/input_imgs')
    animate_line('out/bezier/line_anim/16', size=3, steps=60, stop_points=4)