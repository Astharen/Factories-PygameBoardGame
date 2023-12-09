from data.constants import board_size
from helper.extra_pygame_functions import surrounded_property
from models.game.player import Player


class AI(Player):

    def __init__(self, name, presenter):
        super().__init__(name)
        self.presenter = presenter

    def _creating_goal_graph(self, goal, tile_mapping, turn, recursive_map, list_possible_tiles):
        x = goal[0]
        y = goal[1]
        main_key = str(x) + str(y)
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
        key = str(x) + str(y)

        if key not in recursive_map.keys():
            recursive_map[key] = []
        if main_key != key and key not in recursive_map[main_key]:
            recursive_map[main_key].append(key)
        if side_squared and tile_mapping[x][y].owner == 'black' and key not in list_possible_tiles:
            list_possible_tiles.append(key)

        if not is_x and (y == 0 or y == board_size[1] - 1):
            return None
        elif is_x and (x == 0 or x == board_size[0] - 1):
            return None

        if not side_squared or tile_mapping[x][y].owner != 'black':
            new_square = [x, y]
            if new_square != goal and main_key not in recursive_map[key]:
                recursive_map, list_possible_tiles = self._creating_goal_graph(new_square, tile_mapping, turn,
                                                                               recursive_map, list_possible_tiles)
        return recursive_map, list_possible_tiles

    def _bfs_shortest_path(self, graph, start, goal):
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

    def _looking_for_shortest_path(self, recursive_map, list_possible_tiles, goal):
        min_path = 0
        tile_bought = None

        for idx, tile in enumerate(list_possible_tiles):
            new_path = self._bfs_shortest_path(recursive_map, start=goal, goal=tile)
            len_path = len(new_path)
            if len_path == 0:
                tile_bought = None
            elif len_path < min_path:
                tile_bought = tile
            elif len_path == min_path and tile.type == 'wood':
                tile_bought = tile

        return tile_bought

    def movement(self, list_property, list_color_map, turn, cash, goal_price, n_turns,
                 current_profit, factory_price, exploration_price, goal, wood_profit, factory_profit, factory, wood,
                 goal_enclosed):
        action = 0
        sb_end = False
        if turn == 2:
            jturn = n_turns
            jprofit = current_profit[str(turn)]
            minimum_price = goal_price + jturn / 2
            for iturn in range(int(5 - factory[str(turn)] + 1)):
                minimum_price += jturn / 2 - jprofit + factory_price
                jturn += 2
                jprofit += factory_profit - int(wood_profit / 5)

            minimum_price += jturn / 2

            sided_square, direction = surrounded_property(goal[0], goal[1], turn, list_property, board_size)
            if not sided_square and current_profit[str(turn)] > 20:
                if not goal_enclosed:
                    bought = False
                    recursed_map, list_possible_tiles = self.creating_goal_graph(goal, list_property, board_size, turn,
                                                                                 recursed_map={},
                                                                                 list_possible_tiles=[])
                    position_tile, bought = self.looking_for_shortest_path(recursed_map, list_possible_tiles, goal,
                                                                           list_color_map)
                    list_property, current_profit, wood, cash = self.buying_nearest_tile(position_tile, list_property,
                                                                                         board_size, exploration_price,
                                                                                         turn,
                                                                                         current_profit, wood,
                                                                                         list_color_map, cash,
                                                                                         wood_profit)

                    if not bought:
                        goal_enclosed = True
                    else:
                        action = 1
            elif cash[str(turn)] > minimum_price:
                action = 1
                sided_square, direction = surrounded_property(goal[0], goal[1], turn, list_property, board_size)
                if factory[str(turn)] > 4 and not goal_enclosed:
                    if sided_square:
                        if cash[str(turn)] >= goal_price and cash[str(turn)] > minimum_price:
                            sb_end = True
                            cash[str(turn)] -= goal_price
                        else:
                            return list_property, action, current_profit, wood, factory, list_color_map, sb_end
                else:
                    list_property, list_color_map, cash, current_profit, factory, wood, bought_factory = self.buying_a_factory(
                        board_size, turn, list_color_map, factory,
                        factory_price, cash, current_profit, factory_profit, list_property, wood)

            elif cash[str(turn)] > factory_price and current_profit[str(turn)] > (n_turns / 2) and factory[
                str(turn)] < 5:
                action = 1
                list_property, list_color_map, cash, current_profit, factory, wood, bought_factory = self.buying_a_factory(
                    board_size, turn, list_color_map, factory,
                    factory_price, cash, current_profit, factory_profit, list_property, wood)
                if not bought_factory:
                    action = 1
                    list_property, list_color_map, wood, cash, current_profit = self.exploring(list_property,
                                                                                               list_color_map,
                                                                                               board_size, turn, wood,
                                                                                               current_profit, cash,
                                                                                               wood_profit,
                                                                                               exploration_price)
            else:
                action = 1
                list_property, list_color_map, wood, cash, current_profit = self.exploring(list_property,
                                                                                           list_color_map,
                                                                                           board_size, turn, wood,
                                                                                           current_profit, cash,
                                                                                           wood_profit,
                                                                                           exploration_price)

        return list_property, action, current_profit, wood, factory, list_color_map, sb_end, goal_enclosed

    def exploring(self, list_property, list_color_map, board_size, turn, wood, current_profit, cash, wood_profit,
                  exploration_price):
        wood_list = []
        possible_squares, direction = self.get_possible_square(list_property, list_color_map, board_size, turn)
        ind = 0
        if len(possible_squares['1']) > 0:
            for possibilities in possible_squares['1']:
                wood_list.append(
                    self.region_with_more_wood(possibilities[0], possibilities[1], direction['1'][ind], board_size,
                                               list_color_map, list_property))
                ind += 1
            max_wood = max(wood_list)
            index = wood_list.index(max_wood)
            list_property[possible_squares['1'][index][1]][possible_squares['1'][index][0]] = str(turn)
            wood[str(turn)] += 1
            current_profit[str(turn)] += wood_profit
            cash[str(turn)] -= exploration_price
        else:  # If there's no possible wood square
            for possibilities in possible_squares['0']:
                wood_list.append(
                    self.region_with_more_wood(possibilities[0], possibilities[1], direction['0'][ind], board_size,
                                               list_color_map, list_property))
                ind += 1
            max_wood = max(wood_list)
            index = wood_list.index(max_wood)
            list_property[possible_squares['0'][index][1]][possible_squares['0'][index][0]] = str(turn)
            cash[str(turn)] -= exploration_price
        return list_property, list_color_map, wood, cash, current_profit

    def buying_a_factory(self, board_size, turn, list_color_map, factory, factory_price, cash, current_profit,
                         factory_profit, list_property, wood):
        bought_factory = False
        for y_prop in range(board_size[1]):
            for x_prop in range(board_size[0]):
                if list_property[y_prop][x_prop] == str(turn) and not bought_factory and list_color_map[y_prop][
                    x_prop] == '0':
                    list_color_map[y_prop][x_prop] = '2'
                    cash[str(turn)] -= factory_price
                    current_profit[str(turn)] += factory_profit
                    factory[str(turn)] += 1
                    bought_factory = True
        if not bought_factory:
            for y_prop in range(board_size[1]):
                for x_prop in range(board_size[0]):
                    if list_property[y_prop][x_prop] == str(turn) and not bought_factory and list_color_map[y_prop][
                        x_prop] == '1':
                        list_color_map[y_prop][x_prop] = '2'
                        cash[str(turn)] -= factory_price
                        current_profit[str(turn)] += factory_profit
                        factory[str(turn)] += 1
                        bought_factory = True
                        wood[str(turn)] -= 1
        return list_property, list_color_map, cash, current_profit, factory, wood, bought_factory

    def get_possible_square(self, list_property, list_color_map, board_size, turn):
        possible_squares = {'0': [], '1': []}
        directions = {'0': [], '1': []}
        for y in range(board_size[1]):
            for x in range(board_size[0]):
                if list_property[y][x] == '0':
                    sided_square, direction = surrounded_property(x, y, turn, list_property, board_size)
                    if sided_square:
                        possible_squares[list_color_map[y][x]].append([x, y])
                        directions[list_color_map[y][x]].append(direction)
        return possible_squares, directions

    def region_with_more_wood(self, x, y, direction, board_size, list_color_map, list_property):

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

        for y_reg in range(min(y_dir1, y_dir2), (max(y_dir1, y_dir2) + 1)):
            for x_reg in range(min(x_dir1, x_dir2), (max(x_dir1, x_dir2) + 1)):
                if list_color_map[y_reg][x_reg] == '1' and list_property[y_reg][x_reg] == '0':
                    wood += 1
        return wood

    def calculate_goal_enclosed(self, goal, board_size, list_property):
        goal_enclosed = False
        prop1 = 0
        prop2 = 0
        y1 = max(goal[1] - 1, 0)
        y2 = min(goal[1] + 1, board_size[1] - 1)
        x1 = max(goal[0] - 1, 0)
        x2 = min(goal[0] + 1, board_size[0] - 1)
        for iy in range(y1, y2):
            sided_square1, direction1 = surrounded_property(goal[0], iy, 1, list_property, board_size)
            if sided_square1:
                prop1 += 1
            sided_square2, direction2 = surrounded_property(goal[0], iy, 2, list_property, board_size)
            if sided_square2:
                prop2 += 1
        for ix in range(x1, x2):
            sided_square1, direction1 = surrounded_property(ix, goal[1], 1, list_property, board_size)
            if sided_square1:
                prop1 += 1
            sided_square2, direction2 = surrounded_property(ix, goal[1], 2, list_property, board_size)
            if sided_square2:
                prop2 += 1
        if prop1 == 4 or prop2 == 4:
            goal_enclosed = True
        return goal_enclosed
