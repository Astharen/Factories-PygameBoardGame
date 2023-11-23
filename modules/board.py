from abc import ABC, abstractmethod

from data.constants import board_size


class Board(ABC):

    @property
    @abstractmethod
    def tile_mapping(self):
        pass

    @tile_mapping.setter
    def tile_mapping(self, value):
        self.tile_mapping = value

    def create_board(self):
        for y in range(board_size[1]):
            tile_mapping_x = []
            for x in range(board_size[0]):
                self.add_tile()
            self.tile_mapping.append(tile_mapping_x)

    @abstractmethod
    def add_tile(self):
        pass
