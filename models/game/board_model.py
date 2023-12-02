import random

from data.constants import board_size, n_divisions
from abstract_classes.board import Board
from models.game.tile_model import TileModel


class BoardModel(Board):

    def __init__(self):
        self.tile_mapping = []
        self.wood_squares = self._calc_wood_squares()
        self.init_player_pos = self._calc_init_player_pos()

    @staticmethod
    def _calc_wood_squares():
        wood_squares = []
        for i in range(n_divisions):
            wood_squares += random.sample(range(int(board_size[0] * board_size[1] / n_divisions * i + 1),
                                                int(board_size[0] * board_size[1] / n_divisions * (i + 1))),
                                          int(board_size[0] * board_size[1] / 2 / n_divisions))
        return wood_squares

    def _get_position_tile(self, x, y):
        if (board_size[0] * y + x + 1) in self.wood_squares:
            return TileModel(x, y, "1")
        else:
            return TileModel(x, y, "0")

    @staticmethod
    def _calc_init_player_pos():
        first_x = random.randint(0, board_size[0] - 1)
        first_y = random.randint(0, board_size[1] - 1)
        return first_x, first_y
