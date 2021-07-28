import os
import sys
import pygame
from pygame.locals import *


class Scene:
    # takes Rects, and animations parameters
    # outputs animation as gif, series of png or live in window
    def __init__(self, objects=[], img_size=(800, 800), bg_color=(92, 92, 10)):
        self.objects = objects
        self.img_size = img_size
        self.bg_col = bg_color

    def update_rule(self):
        pass

    def animate(self, dt=0, output_dir=None, fps=60, save_range=None):
        if output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        pygame.init()

        if not dt:
            dt = 1. / fps

        clock = pygame.time.Clock()
        if not output_dir:
            screen = pygame.display.set_mode(self.img_size)
        else:
            screen = pygame.Surface(self.img_size)

        c, unpin_n = 1, 0
        while True:
            self.update_rule()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()



            self.update_bg(screen)
            for r in self.objects:
                r.update(dt)
                r.draw(screen)

            c += 1
            if c > save_range[1]:
                return
            if not c%100:
                print(f'{c}/{save_range[1]}')
            if output_dir:
                if save_range:
                    if save_range[0] <= c <= save_range[1]:
                        pygame.image.save(screen, "{}/pym{}.png".format(output_dir, str(unpin_n).zfill(4)))
                        unpin_n += 1
                else:
                    pygame.image.save(screen, "{}/pym{}.png".format(output_dir, str(c).zfill(4)))
            else:
                pygame.display.update()
            #clock.tick(10)

    def save_imgs(self, steps):

        pass

    def display(self):
        pass

    def update_bg(self, surface):
        #surface.bg = pygame.image.load("bg.png")
        surface.fill(self.bg_col)
        #surface.fill()
        #INSIDE OF THE GAME LOOP
        #gameDisplay.blit(bg, (0, 0))




class SceneBackground(Scene):
    def __init__(self, objects, background_img,  img_size=1000):
        super().__init__(objects=objects, img_size =img_size)
        self.bg = pygame.image.load(background_img)


    def update_bg(self, surface):
        surface.blit(self.bg, (0,0))
