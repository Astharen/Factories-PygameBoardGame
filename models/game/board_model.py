import random

from data.constants import board_size, n_divisions
from abstract_classes.board import Board
from models.game.tile_model import TileModel


class BoardModel(Board):

    def __init__(self):
        self.tile_mapping = []
        self.wood_squares = self._calc_wood_squares()
        self.create_board()

    @staticmethod
    def _calc_wood_squares():
        """
        To ensure a more homogeneous wood tile distribution
        :return:
        """
        wood_squares = []
        for i in range(n_divisions):
            wood_squares += random.sample(range(int(board_size[0] * board_size[1] / n_divisions * i + 1),
                                                int(board_size[0] * board_size[1] / n_divisions * (i + 1))),
                                          int(board_size[0] * board_size[1] / 2 / n_divisions))
        return wood_squares

    def _get_position_tile(self, x, y):
        if (board_size[0] * y + x + 1) in self.wood_squares:
            return TileModel(x, y, '1')
        else:
            return TileModel(x, y, '0')

    @staticmethod
    def set_tile_to_a_player(tile, player):
        tile.set_owner(player)
        player.add_tile(tile)

    def calc_init_player_tile(self):
        not_end = True
        first_tile = None
        while not_end:
            first_x = random.randint(0, board_size[0] - 1)
            first_y = random.randint(0, board_size[1] - 1)
            first_tile = self.tile_mapping[first_x][first_y]
            if first_tile.type == '0' and first_tile.owner is None:
                not_end = False
        return first_tile
