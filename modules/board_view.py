from data.constants import board_size, window_x, window_y, square_size, space_between_squares
from modules.tile_view import TileView


class BoardView:

    def __init__(self):
        self.left_top_y = window_y - board_size[1] * (square_size + space_between_squares) - window_x / 100
        self.tile_mapping = {}

    def get_position_tile(self, x, y):
        return TileView(x, y, self.left_top_y)
