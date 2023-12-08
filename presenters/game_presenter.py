from abstract_classes.presenter import Presenter


class GamePresenter(Presenter):

    def get_tile_mapping(self):
        return self.model.board.tile_mapping

    def get_turn(self):
        return self.model.turn

    def get_language(self):
        return self.model.language

    def get_n_turns(self):
        return self.model.n_turns

    def get_current_player(self):
        return self.model.get_current_player()

    def get_players(self):
        return self.model.players

    def get_taxes(self):
        return self.model.taxes

    def get_game_parameters(self):
        return self.model.game_parameters

    def get_tile_from_position(self, x, y):
        return self.model.board.tile_mapping[x][y]

    def calc_player_tile_exploration(self, tile_x, tile_y):
        self.model.calc_player_tile_exploration(tile_x, tile_y)
        tile = self.model.board.tile_mapping[tile_x][tile_y]
        self.view.board.tile_mapping[tile_x][tile_y].set_colors(tile)

    def calc_player_factory_buy(self, tile_x, tile_y):
        self.model.calc_player_factory_buy(tile_x, tile_y)
        tile = self.model.board.tile_mapping[tile_x][tile_y]
        self.view.board.tile_mapping[tile_x][tile_y].set_colors(tile)

    def end_turn(self):
        self.model.end_turn()
        players = self.model.players
        players_to_drop = []
        for player in players:
            if player.cash < 0:
                players_to_drop.append(player)
        self.model.drop_player_list(players_to_drop)
        if len(players) <= 1:
            winner = players if len(players) > 0 else None
            self.change_to_end(winner=winner)

    def change_to_end(self, winner):
        self.app.set_window('end', language=self.get_language(), winner=winner, vs_ai=self.model.vs_ai)
