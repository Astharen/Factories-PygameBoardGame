import pygame

from data.constants import window_x, space_between_squares, square_size, color_mapping


class TileView:

    def __init__(self, x, y, left_top_y, tile):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(window_x / 100 + space_between_squares + x * square_size + space_between_squares * x,
                                left_top_y + y * square_size + space_between_squares * y, square_size, square_size)
        self.fill_color = color_mapping[tile.type]
        self.border_color = color_mapping[tile.owner]

    def set_colors(self, tile):
        self.fill_color = color_mapping[tile.type]
        self.border_color = color_mapping[tile.owner]
