import random

from data.constants import board_size, n_divisions
from abstract_classes.board import Board
from models.game.tile_model import TileModel


class BoardModel(Board):

    def __init__(self):
        self.tile_mapping = []
        self.wood_squares = self._calc_wood_squares()
        self.create_board()
        self.goal = None

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
            return TileModel(x, y, 'wood')
        else:
            return TileModel(x, y, 'nothing')

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
            if first_tile.type == 'nothing' and first_tile.owner == 'black':
                not_end = False
        return first_tile

    def set_goal_tile(self, players_initial_tiles):
        n = 0
        is_goal_not_found = True
        first_x = [player_init_tile.x for player_init_tile in players_initial_tiles]
        first_y = [player_init_tile.y for player_init_tile in players_initial_tiles]
        goal_x = max(board_size[0] - 1, int(sum(first_x) / len(first_x)) + random.randint(0, 1))
        goal_y = max(board_size[1] - 1, int(sum(first_y) / len(first_y)) + random.randint(0, 1))
        goal = self.tile_mapping[goal_x][goal_y]
        step = 1
        while is_goal_not_found:
            if goal.owner == 'black':
                is_goal_not_found = False
            else:
                if n % 2 == 0:
                    goal_x += step
                    if goal_x >= board_size[0]:
                        goal_x -= 2
                        step = -1
                if n % 2 == 1:
                    goal_y += 1
                    if goal_y >= board_size[1]:
                        goal_y -= 2
                        step = -1
            goal = self.tile_mapping[goal_x][goal_y]
            n += 1
        goal.type = 'goal'
        self.goal = goal
