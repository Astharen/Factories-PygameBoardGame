import sys

import pygame

from abstract_classes.view import View
from data.constants import board_size, square_size, window_x, window_y, legend_color_text_mapping, \
    top_side_mapping_table, top_side_mapping_right
from helper.extra_pygame_functions import draw_text_top_left, draw_text_centered, surrounded_property, conf_menu
from views.game.board_view import BoardView


class GameView(View):

    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.board = None
        self.run = True

    def start(self):
        self.board = BoardView(self.presenter.get_tile_mapping())

    def main(self):
        while self.run:
            self.screen.fill((50, 50, 50))
            self.clock.tick(30)
            action = 0
            click = False
            sb_end = False
            # goal_enclosed = calculate_goal_enclosed(goal, board_size, list_property)
            self.draw_map()
            self.draw_top_side()
            self.draw_legend()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            # if ia:
            #     list_property, action, current_profit, wood, factory, list_color_map, sb_end, goal_enclosed = movement_IA(
            #         possible_squares, list_property, list_color_map,
            #         board_size, turn, cash, goal_price, n_turns, current_profit, factory_price, exploration_price, goal,
            #         wood_profit, factory_profit, factory, wood, goal_enclosed)

            turn = self.presenter.get_turn()
            list_tile_models = self.presenter.get_tile_mapping()
            language = self.presenter.get_language()
            game_parameters = self.presenter.get_game_parameters()
            player = self.presenter.get_current_player()

            mx, my = pygame.mouse.get_pos()
            for x in range(board_size[0]):
                for y in range(board_size[1]):
                    tile_model = self.presenter.get_tile_from_position(x, y)
                    tile_view = self.board.tile_mapping[x][y]
                    if tile_view.rect.collidepoint((mx, my)) and click:
                        if tile_model.owner == 'black':
                            sided_square, direction = surrounded_property(x, y, turn, list_tile_models, board_size)
                            if sided_square:
                                # self.screenshot = pygame.display.get_surface()
                                if language == 'Spanish':
                                    confirm, conf_pass = conf_menu(self.screen, mx, my,
                                                                   f'Explorar: {game_parameters["exploration_price"]}',
                                                                   window_x, window_y, language)
                                elif language == 'English':
                                    confirm, conf_pass = conf_menu(self.screen, mx, my,
                                                                   f'Explore: {game_parameters["exploration_price"]}',
                                                                   window_x, window_y, language)
                                if confirm and player.cash >= game_parameters["exploration_price"]:
                                    action += 1
                                    self.presenter.calc_player_tile_exploration(x, y)
                                if conf_pass:
                                    action += 1
                        elif f'player{turn}' == tile_model.owner and tile_model.type != 'factory':
                            # self.screenshot = pygame.display.get_surface()
                            factory_price = game_parameters['factory_price']
                            if language == 'Spanish':
                                confirm, conf_pass = conf_menu(self.screen, mx, my, 'Fábrica: ' + str(factory_price),
                                                               window_x, window_y, language)
                            elif language == 'English':
                                confirm, conf_pass = conf_menu(self.screen, mx, my, 'Factory: ' + str(factory_price),
                                                               window_x, window_y, language)
                            if confirm and player.cash >= factory_price:
                                action += 1
                                self.presenter.calc_player_factory_buy(x, y)
                            if conf_pass:
                                action += 1
                        elif tile_model.type == 'goal':
                            sided_square, direction = surrounded_property(x, y, turn, list_tile_models, board_size)
                            if sided_square:
                                goal_price = game_parameters['goal_price']
                                if language == 'Spanish':
                                    confirm, conf_pass = conf_menu(self.screen, mx, my, 'Meta: ' + str(goal_price),
                                                                   window_x,
                                                                   window_y, language)
                                elif language == 'English':
                                    confirm, conf_pass = conf_menu(self.screen, mx, my, 'Goal: ' + str(goal_price),
                                                                   window_x,
                                                                   window_y, language)

                                n_player_factories = player.calc_num_owned_tile_type('factory')
                                if confirm and player.cash >= goal_price and n_player_factories > 4:
                                    sb_end = True
                                    action += 1
            if action == 1:
                if sb_end:
                    self.run = False
                    self.presenter.change_to_end(winner=player)
                else:
                    self.presenter.end_turn()
            pygame.display.update()

    def draw_map(self):
        for y in range(board_size[1]):
            for x in range(board_size[0]):
                tile_view = self.board.tile_mapping[x][y]
                pygame.draw.rect(self.screen, tile_view.fill_color, tile_view.rect)
                pygame.draw.rect(self.screen, tile_view.border_color, tile_view.rect, 3)

    def draw_legend(self):
        left_x = int((square_size + 3) * board_size[0] + 30)
        font_conf = pygame.font.SysFont(None, 20)
        y = self.board.left_top_y + 30

        language = self.presenter.get_language()

        for index in range(len(legend_color_text_mapping['color'])):
            text = legend_color_text_mapping['language'][language][index]
            color = legend_color_text_mapping['color'][index]
            border = legend_color_text_mapping['border'][index]
            draw_text_top_left(text, font_conf, (255, 255, 255), self.screen, left_x + 35, y)
            if border:
                pygame.draw.rect(self.screen, color, (left_x, y, 20, 20), border)
            else:
                pygame.draw.rect(self.screen, color, (left_x, y, 20, 20))
            y += 35

    def draw_top_side(self):

        left_top_y = self.board.left_top_y
        turn = self.presenter.get_turn()
        n_turns = self.presenter.get_n_turns()
        taxes = self.presenter.get_taxes()
        language = self.presenter.get_language()
        players = self.presenter.get_players()
        [player.calc_wood_and_factory() for player in players]

        font_conf = pygame.font.SysFont(None, 20)
        x_table = int(window_x / 3 * 2)
        y_table = left_top_y - int(left_top_y / 10) - 20
        y_table = int(y_table - (y_table % 3))
        height_part = int(y_table / (1 + len(players)))

        text_list = top_side_mapping_table['language'][language]
        x_measurements = [len(text) + 2 for text in text_list]
        x_measurements = [int(x_table * x_meas / sum(x_measurements)) for x_meas in x_measurements]
        x_table = sum(x_measurements)
        pygame.draw.rect(self.screen, (200, 200, 200), (20, 20, x_table, y_table))

        x = 20
        for index in range(len(top_side_mapping_table['language']['English'])):
            x_section = x_measurements[index]
            pygame.draw.rect(self.screen, (0, 0, 0), (x, 20, x_section, height_part), 2)
            draw_text_centered(text_list[index], font_conf, (0, 0, 0), self.screen,
                               x + x_section / 2, 20 + height_part / 2)
            for idx, player in enumerate(players):
                attribute = top_side_mapping_table['attribute'][index]
                text = str(index) if index == 0 else str(getattr(player, attribute))

                pygame.draw.rect(self.screen, (0, 0, 0), (x, 20 + (idx + 1) * height_part, x_section, height_part), 2)
                draw_text_centered(text, font_conf, (0, 0, 0), self.screen, x + x_section / 2,
                                   20 + (idx + 1) * height_part + height_part / 2)
            x += x_section

        x_turn = x_table + 20 + 50
        y = 20
        var_values = {'turn': str(n_turns), 'player_name': str(turn + 1), 'taxes': str(taxes)}
        for right_index in range(len(top_side_mapping_right['var_names'])):
            text = top_side_mapping_right['language'][language][right_index]
            var_name = top_side_mapping_right['var_names'][right_index]
            text = text.replace(f'%s({var_name})', var_values[var_name])
            draw_text_centered(text, font_conf, (255, 255, 255), self.screen, x_turn, y)
            y += 40
