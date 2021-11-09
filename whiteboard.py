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
    def __init__(self, screen_size=(800, 800), pixel_per_data=1):
        pygame.init()
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.whiteboard_image = np.zeros(np.ceil(np.array(screen_size) / pixel_per_data).astype(np.int32)) + 100
        self.pixel_per_data = pixel_per_data
        self.draw_was_active = False
        self.prev_mouse_pos = (0,0)
        self.draw_color = 255
        self.brush_size = 4

    @property
    def normalized_brush_size(self):
        if self.brush_size < 1:
            self.brush_size = 1
        return int(self.brush_size)

    def reset_picture(self):
        self.whiteboard_image = np.zeros(np.ceil(np.array(self.screen_size) / self.pixel_per_data).astype(np.int32))

    def draw_courser(self, pos, size=5, color=(100, 100, 100)):
        surf = pygame.Surface((size,)*2)
        surf.fill(color)
        surf = surf.convert()
        self.screen.blit(surf, pos)

    def draw_point(self, p):
        img_shape = self.whiteboard_image.shape
        if img_shape[0] > p[0] and img_shape[1] > p[1]:
            self.whiteboard_image[int(p[0])][int(p[1])] = self.draw_color

    def draw_around_point(self, point, size=3):
        points = []
        points.append([point[0], point[1]])
        for i in range(1, size):
            def f(n):
                points.append((point[0] + n, point[1]))
                points.append((point[0], point[1] + n))
                points.append((point[0] + n, point[1]+n))
            f(i)
            f(-i)
        for p in points:
            self.draw_point(p)

    def update_image_data_with_draw_input(self):
        mouse_keys = pygame.mouse.get_pressed()
        if mouse_keys[0] == 1:
            pos = np.array(pygame.mouse.get_pos())
            whiteboard_p = pos // self.pixel_per_data
            if not self.draw_was_active:
                self.draw_around_point(whiteboard_p, self.normalized_brush_size)
            else:
                prev_p = self.prev_mouse_pos // self.pixel_per_data
                vec = whiteboard_p - prev_p
                shortening_fac = (np.max(abs(vec)))
                vec = vec / shortening_fac
                for _ in range(abs_ceil(shortening_fac)):
                    prev_p = prev_p + vec
                    self.draw_around_point(prev_p, self.normalized_brush_size)

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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_KP0]:
            self.reset_picture()

        def keydown(event, key):
            return event.type == pygame.KEYDOWN and event.key == key

        for e in pygame.event.get():
            if keydown(e, pygame.K_KP_PLUS):
                self.brush_size += 1
            if keydown(e, pygame.K_KP_MINUS):
                self.brush_size -= 1
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