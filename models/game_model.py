import json
import random

from models.game.player import Player
from models.game.board_model import BoardModel


class GameModel:
    def __init__(self):
        self.players = []
        self.dropped_players = []
        self.board = BoardModel()

        self.game_parameters = self.get_game_parameters()

        self.ended_game = False
        self.vs_ai = None
        self.language = None
        self.turn = None
        self.first_turn = None
        self.n_turns = 1
        self.taxes = self.calc_taxes_by_turn()

    def start(self, vs_ai, language):
        self.language = language
        self.vs_ai = vs_ai
        initial_tiles = self.set_players(vs_ai)
        self.first_turn = random.randint(1, len(self.players))
        self.turn = self.first_turn
        self.board.set_goal_tile(initial_tiles)

    def set_players(self, vs_ai):
        self.add_player(Player('player1'))
        self.add_player(Player('player2'))

        initial_tiles = []

        for player in self.players:
            player_init_tile = self.board.calc_init_player_tile()
            player.start(cash=self.game_parameters['initial_cash'])
            self.board.set_tile_to_a_player(player_init_tile, player)
            initial_tiles.append(player_init_tile)
        return initial_tiles

    @staticmethod
    def get_game_parameters():
        with open('data/game_parameters.txt', 'r') as outfile:
            game_parameters = json.load(outfile)

        return game_parameters

    def add_player(self, player):
        self.players.append(player)

    def get_current_player(self):
        return self.players[self.turn - 1]

    def calc_player_tile_exploration(self, tile_x, tile_y):
        tile = self.board.tile_mapping[tile_x][tile_y]
        player = self.get_current_player()
        player.cash -= self.game_parameters['exploration_price']
        self.board.set_tile_to_a_player(tile, player)

    def calc_player_factory_buy(self, tile_x, tile_y):
        tile = self.board.tile_mapping[tile_x][tile_y]
        player = self.get_current_player()
        tile.type = 'factory'
        player.cash -= self.game_parameters['factory_price']

    def calc_taxes_by_turn(self):
        return int((self.n_turns + 2) * 1 / 2)

    def end_turn(self):
        player = self.get_current_player()
        wood_profit, factory_profit = self.game_parameters['wood_profit'], self.game_parameters['factory_profit']
        n_wood = player.calc_num_owned_tile_type('wood')
        n_factories = player.calc_num_owned_tile_type('factory')
        player.current_profit = wood_profit * n_wood + factory_profit * n_factories
        player.cash += player.current_profit
        if self.n_turns % len(self.players) == 0:
            for p in self.players:
                p.cash -= self.taxes
            self.taxes = self.calc_taxes_by_turn()
        self.turn = (self.n_turns + self.first_turn + 1) % 2 + 1
        self.n_turns += 1

    def drop_player_list(self, players_to_drop):
        for player in players_to_drop:
            self.dropped_players.append(player)
            self.players.remove(player)
