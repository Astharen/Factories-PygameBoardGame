import json

from models.board_model import Board


class Game:
    def __init__(self):
        self.players = []
        self.board = Board()

        (self.factory_price, self.exploration_price, self.wood_profit, self.factory_profit,
         self.initial_cash, self.goal_price) = self.get_game_parameters()

        self.ended_game = False

    @staticmethod
    def get_game_parameters():
        with open('../data/game_parameters.txt', 'r') as outfile:
            data = json.load(outfile)

        factory_price = data['factory_price']
        exploration_price = data['exploration_price']
        wood_profit = data['wood_profit']
        factory_profit = data['factory_profit']
        initial_cash = data['initial_cash']
        goal_price = data['goal_price']
        return factory_price, exploration_price, wood_profit, factory_profit, initial_cash, goal_price

    def add_player(self, player):
        self.players.append(player)

    # Other model-related logic and game state management
