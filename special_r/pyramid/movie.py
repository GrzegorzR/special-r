import pygame




def show_height():
    img_size = (1920, 1080)

    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    myfont = pygame.font.SysFont('Comic Sans MS', 30)



if __name__ == '__main__':
    import pygame
    from pygame.locals import *
    from sys import exit

    # initializing variables
    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 24)

    FONT = pygame.font.SysFont("comicsansms", 24)

    # 26 letters, pygame_key not support for caps
    LETTERS = [chr(i) for i in range(97, 123)]

    # text input in terminal
    text = ""

    start_input = False
    # just use color for show if the input start or end
    terminal_color = (240, 240, 240)
    circle_position = [100, 300]


    def on_event(event):
        global text, terminal_color, start_input, circle_position
        if event.type == QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if mouse_in_terminal_window(pos):
                # input start
                start_input = True
                terminal_color = (0, 0, 0)

        if start_input and pygame.key.get_focused():

            press = pygame.key.get_pressed()

            for i in range(0, len(press)):
                if press[i] == 1:
                    name = pygame.key.name(i)

                    if name == 'return':

                        if text == "left":
                            # change the circle postion from (100, 300) to (150, 300)
                            circle_position[0] += 50

                        # input end
                        start_input = False
                        terminal_color = (240, 240, 240)
                        text = ""

                    elif name in LETTERS:
                        text += name

                    elif name == 'backspace':
                        text = text[:-1] if len(text) > 0 else text


    def on_render():
        screen.fill((255, 255, 255))
        render_terminal()
        render_circle()
        pygame.display.update()


    def render_terminal():
        pygame.draw.rect(screen, terminal_color, (0, 50, 640, 50), 0)
        t = FONT.render(text, True, (255, 255, 255))
        screen.blit(t, (10, 60))


    def render_circle():
        pygame.draw.circle(screen, (0, 0, 0), circle_position, 20, 0)


    def mouse_in_terminal_window(pos):
        if 0 <= pos[0] <= 640 and 50 <= pos[1] <= 100:
            return True
        return False


    while True:
        for event in pygame.event.get():
            on_event(event)
        on_render()