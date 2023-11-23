import random

from data.constants import board_size, n_divisions
from modules.board import Board
from modules.tile import Tile


class BoardModel(Board):

    def __init__(self):
        self.tile_mapping = []
        self.wood_squares = self.calc_wood_squares()

    @staticmethod
    def calc_wood_squares():
        wood_squares = []
        for i in range(n_divisions):
            wood_squares += random.sample(range(int(board_size[0] * board_size[1] / n_divisions * i + 1),
                                                int(board_size[0] * board_size[1] / n_divisions * (i + 1))),
                                          int(board_size[0] * board_size[1] / 2 / n_divisions))
        return wood_squares

    def get_position_tile(self, x, y):
        if (board_size[0] * y + x + 1) in self.wood_squares:
            return Tile(x, y, "1")
        else:
            return Tile(x, y, "0")

    @staticmethod
    def first_position():
        first_x = random.randint(0, board_size[0] - 1)
        first_y = random.randint(0, board_size[1] - 1)
        return first_x, first_y
