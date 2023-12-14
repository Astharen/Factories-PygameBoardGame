from abc import ABC, abstractmethod
from typing import List

from data.constants import board_size


class Board(ABC):

    tile_mapping: List

    def create_board(self):
        for x in range(board_size[0]):
            tile_mapping_x = []
            for y in range(board_size[1]):
                tile = self._get_position_tile(x, y)
                tile_mapping_x.append(tile)
            self.tile_mapping.append(tile_mapping_x)

    @abstractmethod
    def _get_position_tile(self, x, y):
        pass
