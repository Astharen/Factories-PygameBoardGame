import json
import random

from abstract_classes.player import Player
from models.game.board_model import BoardModel


class GameModel:
    def __init__(self):
        self.players = []
        self.board = BoardModel()

        self.game_parameters = self.get_game_parameters()

        self.ended_game = False
        self.language = None
        self.turn = None
        self.taxes = int((0 + 2) * 1/2)

    def start(self, vs_ia, language):
        self.language = language
        self.set_players(vs_ia)
        self.turn = random.randint(1, len(self.players))

    def set_players(self, vs_ia):
        self.players.append(Player('1'))
        self.players.append(Player('2'))

        for player in self.players:
            player_init_tile = self.board.calc_init_player_tile()
            player.start(initial_tile=player_init_tile, cash=self.game_parameters['initial_cash'])

    @staticmethod
    def get_game_parameters():
        with open('../data/game_parameters.txt', 'r') as outfile:
            game_parameters = json.load(outfile)

        return game_parameters

    def add_player(self, player):
        self.players.append(player)

    # Other model-related logic and game state management
