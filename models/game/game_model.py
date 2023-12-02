import json

from models.game.board_model import Board


class GameModel:
    def __init__(self):
        self.players = []
        self.board = Board()

        self.game_parameters = self.get_game_parameters()

        self.ended_game = False

    @staticmethod
    def get_game_parameters():
        with open('../../data/game_parameters.txt', 'r') as outfile:
            game_parameters = json.load(outfile)

        return game_parameters

    def game_variables(self):
        wood = {str(i+1): 0 for i in range(len(self.players))}
        factory = {'1': 0, '2': 0}
        cash = {'1': initial_cash, '2': initial_cash}
        current_profit = {'1': 0, '2': 0}

    def add_player(self, player):
        self.players.append(player)

    # Other model-related logic and game state management
