from special_r.Scene import Scene
from special_r.movie_2.movie_2_objects import Rhombus, ShapeB, Triangle, RhombusFractal


def example_1():
    objects = []
    for i in range(16):
        r = Rhombus(400 + i * 10, 400 + i * 10, 100, 200, color=(15 * i, 200, 200))
        r.scale_self(2 - + 0.1 * i)
        r.rotate_self(0.05 * i)
        # r.rotate_self((math.pi/8)*i)

        objects.append(r)

    s = Scene(objects)
    s.animate()


def example_2():
    objects = []

    r = Rhombus(400, 400, 200, 600, color=(15, 200, 200))
    r = ShapeB(r, 0.5, (0, 0, 0))

    t = Triangle((100., 100.), (200., 250.), (150., 200.))
    t.scale_self(0.)
    t = ShapeB(t, 0.9, (0, 0, 0))
    objects.append(t)
    objects.append(r)

    s = Scene(objects)
    s.animate()

def example_3():
    r = RhombusFractal()
    pass

if __name__ == '__main__':
    example_2()
    #example_2()
