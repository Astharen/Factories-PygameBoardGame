import pygame

from data.constants import window_x, space_between_squares, square_size


class TileView:

    def __init__(self, x, y, left_top_y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(window_x / 100 + space_between_squares + x * square_size + space_between_squares * x,
                                left_top_y + y * square_size + space_between_squares * y, square_size, square_size)
