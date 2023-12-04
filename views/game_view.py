import sys

import pygame

from abstract_classes.view import View
from data.constants import board_size, square_size, window_x, window_y, legend_color_text_mapping
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
            self.draw_leyend()
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
                                    confirm, conf_pass = conf_menu(self.screen, mx, my, 'Meta: ' + str(goal_price), window_x,
                                                                   window_y, language)
                                elif language == 'English':
                                    confirm, conf_pass = conf_menu(self.screen, mx, my, 'Goal: ' + str(goal_price), window_x,
                                                                   window_y, language)

                                n_player_factories = player.calc_num_owned_tile_type('factory')
                                if confirm and player.cash >= goal_price and n_player_factories > 4:
                                    sb_end = True
                                    action += 1
            if action == 1:
                if sb_end:
                    self.run = False
                    winner = True
                    self.presenter.change_to_end_screen(winner)
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

        wood, factory, cash, current_profit = {}, {}, {}, {}
        for idx, player in enumerate(players):
            wood[str(idx + 1)] = player.calc_num_owned_tile_type('wood')
            factory[str(idx + 1)] = player.calc_num_owned_tile_type('factory')
            cash[str(idx + 1)] = player.cash
            current_profit[str(idx + 1)] = player.current_profit

        font_conf = pygame.font.SysFont(None, 20)
        x_table = int(window_x/3*2)
        y_table = left_top_y - int(left_top_y/10) - 20
        y_table = int(y_table - (y_table%3))
        heigth_part = int(y_table/3)
        spanish_text = ['Madera', 'Fábrica', 'Dinero', 'Beneficios', 'Turno: ', 'Turno de: ' + str(turn), 'Impuestos: ']
        english_text = ['Wood', 'Factory', 'Money', 'Profit', 'Turn: ', str(turn) + '\'s turn', 'Taxes: ']
        index = 0
        if language == 'Spanish':
            text_list = spanish_text
            x_total_parts = 3 + 8 + 9 + 8 + 11# This has been calculated by counting the number of letter in each word and adding 2 (1 for each space)
            # The words were: one number, madera, fábrica, dinero, beneficio
            x_player = int(x_table * 3 / x_total_parts)
            x_wood = int(x_table * 8 / x_total_parts)
            x_factory = int(x_table * 9 / x_total_parts)
            x_cash = int(x_table * 8 / x_total_parts)
            x_profit = int(x_table * 11 / x_total_parts)
            x_table = int(x_player + x_wood + x_factory + x_cash + x_profit)
            pygame.draw.rect(self.screen, (200, 200, 200), (20, 20,  x_table, y_table))
        elif language == 'English':
            text_list = english_text
            x_total_parts = 3 + 6 + 9 + 7 + 8
            # This has been calculated by counting the number of letter in each word and adding 2 (1 for each space)
            # The words were: one number, wood, factory, money, profit
            x_player = int(x_table * 3 / x_total_parts)
            x_wood = int(x_table * 6 / x_total_parts)
            x_factory = int(x_table * 9 / x_total_parts)
            x_cash = int(x_table * 7 / x_total_parts)
            x_profit = int(x_table * 8 / x_total_parts)
            x_table = int(x_player + x_wood + x_factory + x_cash + x_profit)
            pygame.draw.rect(self.screen, (200, 200, 200), (20, 20,  x_table, y_table))
        x = 20
        # Player
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 20, x_player, heigth_part), 2)
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 20 + heigth_part, x_player, heigth_part), 2)
        draw_text_centered('1', font_conf, (0, 0, 0), self.screen, x + x_player/2, 20 + heigth_part + heigth_part/2)
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 20 + 2*heigth_part, x_player, heigth_part), 2)
        draw_text_centered('2', font_conf, (0, 0, 0), self.screen, x + x_player/2, 20 + 2*heigth_part + heigth_part/2)
        x += x_player
        # Wood
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 20, x_wood, heigth_part), 2)
        draw_text_centered(text_list[index], font_conf, (0, 0, 0), self.screen, x + x_wood/2, 20 + heigth_part/2)
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 20 + heigth_part, x_wood, heigth_part), 2)
        draw_text_centered(str(wood['1']), font_conf, (0, 0, 0), self.screen, x + x_wood/2, 20 + heigth_part + heigth_part/2)
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 20 + 2*heigth_part, x_wood, heigth_part), 2)
        draw_text_centered(str(wood['2']), font_conf, (0, 0, 0), self.screen, x + x_wood/2, 20 + 2*heigth_part + heigth_part/2)
        x += x_wood
        index += 1
        # F actory
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 20, x_factory, heigth_part), 2)
        draw_text_centered(text_list[index], font_conf, (0, 0, 0), self.screen, x + x_factory/2, 20 + heigth_part/2)
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 20 + heigth_part, x_factory, heigth_part), 2)
        draw_text_centered(str(factory['1']), font_conf, (0, 0, 0), self.screen, x + x_factory/2, 20 + heigth_part + heigth_part/2)
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 20 + 2*heigth_part, x_factory, heigth_part), 2)
        draw_text_centered(str(factory['2']), font_conf, (0, 0, 0), self.screen, x + x_factory/2, 20 + 2*heigth_part + heigth_part/2)
        x += x_factory
        index += 1
        # Cash
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 20, x_cash, heigth_part), 2)
        draw_text_centered(text_list[index], font_conf, (0, 0, 0), self.screen, x + x_cash/2, 20 + heigth_part/2)
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 20 + heigth_part, x_cash, heigth_part), 2)
        draw_text_centered(str(cash['1']), font_conf, (0, 0, 0), self.screen, x + x_cash/2, 20 + heigth_part + heigth_part/2)
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 20 + 2*heigth_part, x_cash, heigth_part), 2)
        draw_text_centered(str(cash['2']), font_conf, (0, 0, 0), self.screen, x + x_cash/2, 20 + 2*heigth_part + heigth_part/2)
        x += x_cash
        index += 1
        # Profit
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 20, x_profit, heigth_part), 2)
        draw_text_centered(text_list[index], font_conf, (0, 0, 0), self.screen, x + x_profit/2, 20 + heigth_part/2)
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 20 + heigth_part, x_profit, heigth_part), 2)
        draw_text_centered(str(current_profit['1']), font_conf, (0, 0, 0), self.screen, x + x_profit/2, 20 + heigth_part + heigth_part/2)
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 20 + 2*heigth_part, x_profit, heigth_part), 2)
        draw_text_centered(str(current_profit['2']), font_conf, (0, 0, 0), self.screen, x + x_profit/2, 20 + 2*heigth_part + heigth_part/2)
        index += 1
        # Turns
        x_turn = x_table + 20 + 50
        draw_text_centered(text_list[index] + str(n_turns), font_conf, (255, 255, 255), self.screen, x_turn, 20)
        index += 1
        draw_text_centered(text_list[index], font_conf, (255, 255, 255), self.screen, x_turn, 60)
        index += 1
        draw_text_centered(text_list[index] + str(taxes), font_conf, (255, 255, 255), self.screen, x_turn, 100)
