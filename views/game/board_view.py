from data.constants import board_size, window_x, window_y, square_size, space_between_squares
from abstract_classes.board import Board
from views.game.tile_view import TileView


class BoardView(Board):

    def __init__(self, tile_mapping_model):
        self.left_top_y = window_y - board_size[1] * (square_size + space_between_squares) - window_x / 100
        self.tile_mapping = []
        self.tile_mapping_model = tile_mapping_model
        self.create_board()

    def _get_position_tile(self, x, y):
        return TileView(x, y, self.left_top_y, self.tile_mapping_model[x][y])
