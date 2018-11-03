import pygame
import numpy as np
import math


def sign(x):
    if x == 0:
        return 1
    r = x / math.fabs(x)
    return int(r)


def abs_ceil(x):
    return int(sign(x) * math.ceil(math.fabs(x)))


class WhiteBoard:
    def __init__(self, screen_size=(800, 800), pixel_per_data=5):
        pygame.init()
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.whiteboard_image = np.zeros(np.ceil(np.array(screen_size) / pixel_per_data).astype(np.int32)) + 100
        self.pixel_per_data = pixel_per_data
        self.draw_was_active = False
        self.prev_mouse_pos = (0,0)

    def reset_picture(self):
        self.whiteboard_image = np.zeros(self.screen_size, 3)

    def draw_courser(self, pos, size=5, color=(100, 100, 100)):
        surf = pygame.Surface((size,)*2)
        surf.fill(color)
        surf = surf.convert()
        self.screen.blit(surf, pos)

    def update_image_data_with_draw_input(self):
        mouse_keys = pygame.mouse.get_pressed()
        if mouse_keys[0] == 1:
            pos = np.array(pygame.mouse.get_pos())
            whiteboard_p = pos // self.pixel_per_data
            if not self.draw_was_active:
                self.whiteboard_image[int(whiteboard_p[0])][int(whiteboard_p[1])] = 255
            else:
                prev_p = self.prev_mouse_pos // self.pixel_per_data
                vec = whiteboard_p - prev_p
                shortening_fac = (np.max(abs(vec)))
                vec = vec / shortening_fac
                for _ in range(abs_ceil(shortening_fac)):
                    prev_p = prev_p + vec
                    self.whiteboard_image[int(prev_p[0])][int(prev_p[1])] = 255
            self.prev_mouse_pos = pos
            self.draw_was_active = True
        else:
            self.draw_was_active = False

    def draw_whiteboard(self):
        surf = pygame.surfarray.make_surface(self.whiteboard_image)
        surf = surf.convert()
        surf = pygame.transform.scale(surf, self.screen_size)
        self.screen.blit(surf, (0, 0))

    def draw_image(self):
        self.draw_whiteboard()

    def update_loop(self):
        pygame.event.pump()
        self.update_image_data_with_draw_input()
        self.draw_image()
        pygame.display.flip()

    def start_loop(self):
        while True:
            self.update_loop()


def run():
    wb = WhiteBoard()
    while True:
        wb.update_loop()


if __name__ == '__main__':
    run()