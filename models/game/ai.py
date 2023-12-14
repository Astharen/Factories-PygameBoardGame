from data.constants import board_size
from helper.extra_pygame_functions import surrounded_property
from models.game.player import Player


class AI(Player):

    def __init__(self, name):
        super().__init__(name)
        self.presenter = None

    def set_presenter(self, presenter):
        self.presenter = presenter

    def _creating_goal_graph(self, goal, tile_mapping, turn, recursive_map, list_possible_tiles):
        x = goal.x
        y = goal.y
        main_key = (x, y)
        recursive_map[main_key] = []
        for y_sur in range(y - 1, y + 2):
            y_sur = min(y_sur, board_size[1] - 1)
            y_sur = max(y_sur, 0)
            result = self._step_of_creating_goal_graph(x, y_sur, turn, tile_mapping, recursive_map, main_key,
                                                       list_possible_tiles, goal, is_x=False)
            if result is None:
                break
            else:
                recursive_map, list_possible_tiles = result

        for x_sur in range(x - 1, x + 2):
            x_sur = min(x_sur, board_size[0] - 1)
            x_sur = max(x_sur, 0)
            result = self._step_of_creating_goal_graph(x_sur, y, turn, tile_mapping, recursive_map, main_key,
                                                       list_possible_tiles, goal, is_x=True)
            if result is None:
                break
            else:
                recursive_map, list_possible_tiles = result

        return recursive_map, list_possible_tiles

    def _step_of_creating_goal_graph(self, x, y, turn, tile_mapping, recursive_map, main_key, list_possible_tiles, goal,
                                     is_x):
        side_squared, _ = surrounded_property(x, y, turn, tile_mapping)
        key = (x, y)

        if key not in recursive_map.keys():
            recursive_map[key] = []
        if main_key != key and key not in recursive_map[main_key]:
            recursive_map[main_key].append(key)
        if side_squared and tile_mapping[x][y].owner == 'black' and key not in list_possible_tiles:
            list_possible_tiles.append(tile_mapping[x][y])

        if not is_x and (y == 0 or y == board_size[1] - 1):
            return None
        elif is_x and (x == 0 or x == board_size[0] - 1):
            return None

        if not side_squared or tile_mapping[x][y].owner != 'black':
            new_square = tile_mapping[x][y]
            if new_square != goal and main_key not in recursive_map[key]:
                recursive_map, list_possible_tiles = self._creating_goal_graph(new_square, tile_mapping, turn,
                                                                               recursive_map, list_possible_tiles)
        return recursive_map, list_possible_tiles

    @staticmethod
    def _bfs_shortest_path(graph, start, goal):
        explored = []
        queue = [[start]]

        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node not in explored:
                neighbours = graph[node]
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    if neighbour == goal:
                        return new_path

                explored.append(node)
        return []

    @staticmethod
    def _looking_for_shortest_path(recursive_map, list_possible_tiles, goal):
        min_path = 0
        tile_bought = None

        for idx, tile in enumerate(list_possible_tiles):
            new_path = AI._bfs_shortest_path(recursive_map, start=goal, goal=tile)
            len_path = len(new_path)
            if len_path == 0:
                tile_bought = None
            elif len_path < min_path:
                tile_bought = tile
            elif len_path == min_path and tile.type == 'wood':
                tile_bought = tile

        return tile_bought

    def movement(self):
        action = 0
        sb_end = False
        tiles_mapping_model = self.presenter.get_tile_mapping()
        goal = self.presenter.get_goal()
        goal_enclosed = self._calculate_goal_enclosed(goal, tiles_mapping_model)
        game_parameters = self.presenter.get_game_parameters()

        factory_price = game_parameters['factory_price']
        factory_profit = game_parameters['factory_profit']
        wood_profit = game_parameters['wood_profit']
        goal_price = game_parameters['goal_price']

        n_turns = self.presenter.get_n_turns()
        jturn = n_turns
        jprofit = self.current_profit
        minimum_price = goal_price + jturn / 2
        self.calc_wood_and_factory()
        for iturn in range(int(5 - self.factory + 1)):
            minimum_price += jturn / 2 - jprofit + factory_price
            jturn += 2
            jprofit += factory_profit - int(wood_profit / 5)

        minimum_price += jturn / 2

        turn = self.presenter.get_turn()
        sided_square, direction = surrounded_property(goal.x, goal.y, turn, tiles_mapping_model)
        if not sided_square and self.current_profit > 20:
            if not goal_enclosed:
                recursive_map, list_possible_tiles = self._creating_goal_graph(goal, tiles_mapping_model, turn,
                                                                               recursive_map={},
                                                                               list_possible_tiles=[])
                position_tile = self._looking_for_shortest_path(recursive_map, list_possible_tiles, goal)
                self.presenter.calc_player_tile_exploration(*position_tile)
                action = 1
                return action, sb_end
        elif self.cash > minimum_price:
            sided_square, direction = surrounded_property(goal.x, goal.y, turn, tiles_mapping_model)
            if self.factory > 4 and not goal_enclosed:
                if sided_square:
                    if self.cash >= goal_price and self.cash > minimum_price:
                        sb_end = True
                        action = 1
                        return action, sb_end
                    else:
                        return action, sb_end
            else:
                action = self._buying_a_factory()

        elif (self.cash > factory_price and self.current_profit > (n_turns / 2)
              and self.factory < 5):
            action = self._buying_a_factory()
            if action == 0:
                action = self._exploring()
        else:
            action = self._exploring()

        if action == 0:
            action = 1
        return action, sb_end

    def _exploring(self):
        if self.cash < self.presenter.get_game_parameters()['exploration_price']:
            return 0
        action = 0
        wood_list = []
        possible_squares, direction = self._get_possible_square()
        for ind, possibilities in enumerate(possible_squares['wood']):
            wood_list.append(
                self._calc_region_with_more_wood(possibilities[0], possibilities[1], direction['wood'][ind]))

        if len(wood_list):
            max_wood = max(wood_list)
            index = wood_list.index(max_wood)
            action = 1
            self.presenter.calc_player_tile_exploration(*possible_squares['wood'][index])
            return action

        for ind, possibilities in enumerate(possible_squares['nothing']):
            wood_list.append(
                self._calc_region_with_more_wood(possibilities[0], possibilities[1], direction['nothing'][ind]))

        if len(wood_list):
            max_wood = max(wood_list)
            index = wood_list.index(max_wood)
            action = 1
            self.presenter.calc_player_tile_exploration(*possible_squares['nothing'][index])
        return action

    def _buying_a_factory(self):
        if len(self.owned_tiles) == 0 or self.cash < self.presenter.get_game_parameters()['factory_price']:
            return 0
        tile_to_buy = self.owned_tiles[0]
        action = 0
        for tile in self.owned_tiles[1:]:
            if tile.type != 'factory' and tile_to_buy.type == 'factory':
                tile_to_buy = tile
                action = 1
            elif tile_to_buy.type == 'wood' and tile.type == 'nothing':
                tile_to_buy = tile
                action = 1

        self.presenter.calc_player_factory_buy(tile_to_buy.x, tile_to_buy.y)
        return action

    def _get_possible_square(self):
        tile_mapping_model = self.presenter.get_tile_mapping()
        possible_squares = {'nothing': [], 'wood': []}
        directions = {'nothing': [], 'wood': []}
        for x in range(board_size[0]):
            for y in range(board_size[1]):
                if tile_mapping_model[x][y].owner == 'black' and tile_mapping_model[x][y].type != 'goal':
                    turn = self.presenter.get_turn()
                    sided_square, direction = surrounded_property(x, y, turn, tile_mapping_model)
                    if sided_square:
                        possible_squares[tile_mapping_model[x][y].type].append((x, y))
                        directions[tile_mapping_model[x][y].type].append(direction)
        return possible_squares, directions

    def _calc_region_with_more_wood(self, x, y, direction):

        wood = 0
        y_dir1 = y + direction[1] - 1
        y_dir2 = y + direction[1] + 1

        if max(y_dir1, y_dir2) > (board_size[1] - 1):
            supp_y = max(y_dir1, y_dir2) - board_size[1] + 1
            y_dir1 -= supp_y
            y_dir2 -= supp_y

        if min(y_dir1, y_dir2) < 0:
            supp_y = 0 - min(y_dir1, y_dir2)
            y_dir1 += supp_y
            y_dir2 += supp_y

        x_dir1 = x + direction[0] - 1
        x_dir2 = x + direction[0] + 1

        if max(x_dir1, x_dir2) > (board_size[0] - 1):
            supp_x = max(x_dir1, x_dir2) - board_size[0] + 1
            x_dir1 -= supp_x
            x_dir2 -= supp_x

        if min(x_dir1, x_dir2) < 0:
            supp_x = 0 - min(x_dir1, x_dir2)
            x_dir1 += supp_x
            x_dir2 += supp_x

        tile_mapping = self.presenter.get_tile_mapping()

        for y_reg in range(min(y_dir1, y_dir2), (max(y_dir1, y_dir2) + 1)):
            for x_reg in range(min(x_dir1, x_dir2), (max(x_dir1, x_dir2) + 1)):
                if tile_mapping[x_reg][y_reg].type == 'wood' and tile_mapping[x_reg][y_reg].owner == 'black':
                    wood += 1
        return wood

    @staticmethod
    def _calculate_goal_enclosed(goal, tile_mapping):
        goal_enclosed = False
        prop1 = 0
        prop2 = 0
        x1, y1 = max(goal.x - 1, 0), max(goal.y - 1, 0)
        x2, y2 = min(goal.x + 1, board_size[0] - 1), min(goal.y + 1, board_size[1] - 1)

        for iy in range(y1, y2):
            sided_square1, direction1 = surrounded_property(goal.x, iy, 1, tile_mapping)
            if sided_square1:
                prop1 += 1
            sided_square2, direction2 = surrounded_property(goal.x, iy, 2, tile_mapping)
            if sided_square2:
                prop2 += 1
        for ix in range(x1, x2):
            sided_square1, direction1 = surrounded_property(ix, goal.y, 1, tile_mapping)
            if sided_square1:
                prop1 += 1
            sided_square2, direction2 = surrounded_property(ix, goal.y, 2, tile_mapping)
            if sided_square2:
                prop2 += 1
        if prop1 == 4 or prop2 == 4:
            goal_enclosed = True
        return goal_enclosed
