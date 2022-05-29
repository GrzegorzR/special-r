import drawSvg as draw


def add_roz(surface, x, y, s):
    rot_x, rot_y = x+(s/2), -y -(s/2)

    for i in range(0, 10):
        r = draw.Rectangle(x, y, s, s, fill='#12{}ff'.format(str(i * 10)),
                           transform='rotate({} {} {}) '.format(str(i * 10), str(rot_x), str(rot_y)),
                           )

        surface.append(r)

def draw_roz(scale, name):
    d = draw.Drawing(900, 900, origin='center', transform='scale({}) translate(-50 50)'.format(str(scale)),  displayInline=False)
    d.append( draw.Rectangle(-900, -900, 1800, 1800, fill='#222222'))
    add_roz(d, 0,10,40)
    add_roz(d, 100, 100, 80)
    add_roz(d, 50, 50, 20)
    add_roz(d, -50, -50, 20)
    d.setRenderSize(1800,1800)  # Alternative to setPixelScale
    #d.saveSvg('{}.svg'.format(name))
    d.savePng('out/{}.png'.format(name))



if __name__ == '__main__':
    steps = list(range(1000)) + list(reversed(range(1000)))

    for i, v in enumerate(steps):
        print(i)

        draw_roz(1 + 0.015*v, 'example_{}'.format(str(i).zfill(4)))

