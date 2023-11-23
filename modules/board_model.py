import random

from data.constants import board_size, n_divisions
from modules.board import Board


class BoardModel(Board):

    def __init__(self):
        self.tile_mapping = []

    @staticmethod
    def calc_wood_squares():
        wood_squares = []
        for i in range(n_divisions):
            wood_squares += random.sample(range(int(board_size[0] * board_size[1] / n_divisions * i + 1),
                                                int(board_size[0] * board_size[1] / n_divisions * (i + 1))),
                                          int(board_size[0] * board_size[1] / 2 / n_divisions))
        return wood_squares

    def add_tile(self):
        pass

    @staticmethod
    def first_position():
        first_x = random.randint(0, board_size[0] - 1)
        first_y = random.randint(0, board_size[1] - 1)
        return first_x, first_y
