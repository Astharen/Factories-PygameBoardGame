from general_use import surrounded_property

def creating_goal_graph(goal, list_property, board_size, turn, recursed_map, list_possible_tiles):
    y = goal[1]
    x = goal[0]
    main_key = str(x) + str(y)
    recursed_map[main_key] = []
    continuo_recusing = True
    for y_sur in range(y-1,y+2):
        y_sur = min(y_sur, board_size[1]-1)
        y_sur = max(y_sur, 0)
        side_squared, _ = surrounded_property(x, y_sur, turn, list_property, board_size)
        key = str(x) + str(y_sur)
        
        if key not in recursed_map.keys():
            recursed_map[key] = []
        if main_key!=key and key not in recursed_map[main_key]:
            recursed_map[main_key].append(key)
        if side_squared and list_property[y_sur][x]=='0' and key not in list_possible_tiles:
            list_possible_tiles.append(key)

        if y_sur == 0 or y_sur == board_size[1] - 1:
            break
        if not side_squared or list_property[y_sur][x]!='0':
            new_square = [x, y_sur]
            if new_square!=goal and main_key not in recursed_map[key]:
                recursed_map, list_possible_tiles = creating_goal_graph(new_square, list_property, board_size, turn, recursed_map, list_possible_tiles)

    for x_sur in range(x-1, x+2):
        x_sur = min(x_sur, board_size[0]-1)
        x_sur = max(x_sur, 0)
        side_squared, _ = surrounded_property(x_sur, y, turn, list_property, board_size)
        key = str(x_sur) + str(y)

        if key not in recursed_map.keys():
            recursed_map[key] = []
        if main_key!=key and key not in recursed_map[main_key]:
            recursed_map[main_key].append(key)
        
        if side_squared and list_property[y][x_sur]=='0' and key not in list_possible_tiles:
            list_possible_tiles.append(key)
        
        if x_sur == 0 or x_sur == board_size[0] - 1:
            break
        if not side_squared or list_property[y][x_sur]!='0':
            new_square = [x_sur, y]
            if new_square!=goal and main_key not in recursed_map[key]:
                recursed_map, list_possible_tiles = creating_goal_graph(new_square, list_property, board_size, turn, recursed_map, list_possible_tiles)

    return recursed_map, list_possible_tiles

def bfs_shortest_path(graph, start, goal):

    explored = []
    queue = [[start]]
    possible_paths = []
    bought = False

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
                    bought = True
                    return new_path, bought

            explored.append(node)
    return [], bought

def buying_nearest_tile(position_tile, list_property, board_size, exploration_price, turn, current_profit, wood, list_color_map, cash, wood_profit):
    list_property[position_tile[1]][position_tile[0]] = str(turn)
    cash[str(turn)] -= exploration_price
    if list_color_map[position_tile[1]][position_tile[0]] == '1':
        wood[str(turn)] += 1
        current_profit[str(turn)] += wood_profit

    return list_property, current_profit, wood, cash

def looking_for_shortest_path(recursed_map, list_possible_tiles, goal, list_color_map):
    ind = 0
    final_ind = 0
    min_path = 0
    final_bought = False
    for tile in list_possible_tiles:
        start = str(goal[0]) + str(goal[1])
        finish_tile = tile
        new_path, bought = bfs_shortest_path(recursed_map, start, finish_tile)
        len_path = len(new_path)
        if len_path < min_path:
            min_path = len_path
            final_ind = ind
        elif len_path == min_path:
            if list_color_map[int(tile[1])][int(tile[0])] == '1':
                min_path = len_path
                final_ind = ind
        ind += 1
        if bought:
            final_bought = True
    return [int(list_possible_tiles[final_ind][0]), int(list_possible_tiles[final_ind][1])], final_bought


def movement_IA(possible_squares, list_property, list_color_map, board_size, turn, cash, goal_price,
 n_turns, current_profit, factory_price, exploration_price, goal, wood_profit, factory_profit, factory,
 wood, goal_enclosed):
    action = 0
    sb_end = False
    if turn == 2:
        jturn = n_turns
        jprofit = current_profit[str(turn)]
        minimum_price = goal_price +  jturn/2
        for iturn in range(int(5-factory[str(turn)] + 1)):
            minimum_price +=  jturn/2 - jprofit + factory_price
            jturn += 2
            jprofit += factory_profit - int(wood_profit/5)
        
        minimum_price += jturn/2

        sided_square, direction = surrounded_property(goal[0], goal[1], turn, list_property, board_size)
        if not sided_square and current_profit[str(turn)]>20:
            if not goal_enclosed:
                bought = False
                recursed_map, list_possible_tiles = creating_goal_graph(goal, list_property, board_size, turn, recursed_map={}, list_possible_tiles=[])
                position_tile, bought = looking_for_shortest_path(recursed_map, list_possible_tiles, goal, list_color_map)
                list_property, current_profit, wood, cash = buying_nearest_tile(position_tile, list_property, board_size, exploration_price, turn, current_profit, wood, list_color_map, cash, wood_profit)

                if not bought:
                    goal_enclosed = True
                else:
                    action = 1
        elif cash[str(turn)] > minimum_price:
            action = 1
            sided_square, direction = surrounded_property(goal[0], goal[1], turn, list_property, board_size)
            if factory[str(turn)] > 4 and not goal_enclosed:
                if sided_square:
                    if cash[str(turn)] >= goal_price and cash[str(turn)]>minimum_price:
                        sb_end = True
                        cash[str(turn)] -= goal_price
                    else:
                        return list_property, action, current_profit, wood, factory, list_color_map, sb_end
            else:
                list_property, list_color_map, cash, current_profit, factory, wood, bought_factory = buying_a_factory(board_size, turn, list_color_map, factory, 
                factory_price, cash, current_profit, factory_profit, list_property, wood)

        elif cash[str(turn)] > factory_price and current_profit[str(turn)] > (n_turns/2) and factory[str(turn)] < 5:
            action = 1
            list_property, list_color_map, cash, current_profit, factory, wood, bought_factory = buying_a_factory(board_size, turn, list_color_map, factory, 
                factory_price, cash, current_profit, factory_profit, list_property, wood)
            if not bought_factory:
                action = 1
                list_property, list_color_map, wood, cash, current_profit = exploring(list_property, list_color_map, board_size, turn, wood, current_profit, cash, 
                wood_profit, exploration_price)
        else:
            action = 1
            list_property, list_color_map, wood, cash, current_profit = exploring(list_property, list_color_map, board_size, turn, wood, current_profit, cash, 
            wood_profit, exploration_price)

    return list_property, action, current_profit, wood, factory, list_color_map, sb_end, goal_enclosed

def exploring(list_property, list_color_map, board_size, turn, wood, current_profit, cash, wood_profit, exploration_price):
    wood_list = []
    possible_squares, direction = get_possible_square(list_property, list_color_map, board_size, turn)
    ind = 0
    if len(possible_squares['1'])>0:
        for possibilities in possible_squares['1']:
            wood_list.append(region_with_more_wood(possibilities[0], possibilities[1], direction['1'][ind], board_size, list_color_map, list_property))
            ind += 1
        max_wood = max(wood_list)
        index = wood_list.index(max_wood)
        list_property[possible_squares['1'][index][1]][possible_squares['1'][index][0]] = str(turn)
        wood[str(turn)] += 1
        current_profit[str(turn)] += wood_profit
        cash[str(turn)] -= exploration_price
    else: # If there's no possible wood square
        for possibilities in possible_squares['0']:
            wood_list.append(region_with_more_wood(possibilities[0], possibilities[1], direction['0'][ind], board_size, list_color_map, list_property))
            ind += 1
        max_wood = max(wood_list)
        index = wood_list.index(max_wood)
        list_property[possible_squares['0'][index][1]][possible_squares['0'][index][0]] = str(turn)
        cash[str(turn)] -= exploration_price
    return list_property, list_color_map, wood, cash, current_profit

def buying_a_factory(board_size, turn, list_color_map, factory, factory_price, cash, current_profit, factory_profit, list_property, wood):
    bought_factory = False
    for y_prop in range(board_size[1]):
        for x_prop in range(board_size[0]):
            if list_property[y_prop][x_prop] == str(turn) and not bought_factory and list_color_map[y_prop][x_prop]=='0':
                list_color_map[y_prop][x_prop] = '2'
                cash[str(turn)] -= factory_price
                current_profit[str(turn)] += factory_profit
                factory[str(turn)] += 1
                bought_factory = True
    if not bought_factory:
        for y_prop in range(board_size[1]):
            for x_prop in range(board_size[0]):
                if list_property[y_prop][x_prop] == str(turn) and not bought_factory and list_color_map[y_prop][x_prop]=='1':
                    list_color_map[y_prop][x_prop] = '2'
                    cash[str(turn)] -= factory_price
                    current_profit[str(turn)] += factory_profit
                    factory[str(turn)] += 1
                    bought_factory = True
                    wood[str(turn)] -= 1
    return list_property, list_color_map, cash, current_profit, factory, wood, bought_factory

def get_possible_square(list_property, list_color_map, board_size, turn):
    possible_squares = {'0': [], '1': []}
    directions = {'0': [], '1': []}
    for y in range(board_size[1]):
        for x in range(board_size[0]):
            if list_property[y][x]=='0':
                sided_square, direction = surrounded_property(x, y, turn, list_property, board_size)
                if sided_square:
                    possible_squares[list_color_map[y][x]].append([x,y])
                    directions[list_color_map[y][x]].append(direction)
    return possible_squares, directions

def region_with_more_wood(x, y, direction, board_size, list_color_map, list_property):

    wood = 0
    y_dir1 = y + direction[1] - 1
    y_dir2 = y + direction[1] + 1

    if max(y_dir1, y_dir2)>(board_size[1]-1):
        supp_y = max(y_dir1, y_dir2) - board_size[1] + 1
        y_dir1 -= supp_y
        y_dir2 -= supp_y

    if min(y_dir1, y_dir2) < 0:
        supp_y = 0 - min(y_dir1, y_dir2)
        y_dir1 += supp_y
        y_dir2 += supp_y
    
    x_dir1 = x + direction[0] - 1
    x_dir2 = x + direction[0] + 1

    if max(x_dir1, x_dir2)>(board_size[0]-1):
        supp_x = max(x_dir1, x_dir2) - board_size[0] + 1
        x_dir1 -= supp_x
        x_dir2 -= supp_x
    
    if min(x_dir1, x_dir2) < 0:
        supp_x = 0 - min(x_dir1, x_dir2)
        x_dir1 += supp_x
        x_dir2 += supp_x

    for y_reg in range(min(y_dir1, y_dir2), (max(y_dir1, y_dir2)+1)):
        for x_reg in range(min(x_dir1, x_dir2), (max(x_dir1, x_dir2)+1)):
            if list_color_map[y_reg][x_reg] == '1' and list_property[y_reg][x_reg] == '0':
                wood += 1
    return wood

def calculate_goal_enclosed(goal, board_size, list_property):
    goal_enclosed = False
    prop1 = 0
    prop2 = 0
    y1 = max(goal[1]-1, 0)
    y2 = min(goal[1]+1, board_size[1]-1)
    x1 = max(goal[0]-1, 0)
    x2 = min(goal[0]+1, board_size[0]-1)
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
    if prop1 == 4 or prop2==4:
        goal_enclosed = True
    return goal_enclosed