from general_use import surrounded_property

def buy_surrounding_goal(goal, list_property, board_size, exploration_price, turn, current_profit, wood, list_color_map, bought, cash, recursed_map, n_paths, wood_profit):
    y = goal[1]
    x = goal[0]
    key = str(x) + str(y)
    recursed_map[key] = 0
    for y_sur in range(y-1,y+2):
        y_sur = min(y_sur, board_size[0]-1)
        y_sur = max(y_sur, 0)
        side_squared, _ = surrounded_property(x, y_sur, turn, list_property, board_size)
        key = str(x) + str(y_sur)
        
        if key not in recursed_map.keys():
            recursed_map[key] = n_paths
            n_paths += 1
            if side_squared and not bought and list_property[y_sur][x]=='0':
                bought = True
                list_property[y_sur][x] = str(turn)
                cash[str(turn)] -= exploration_price
                if list_color_map[y_sur][x] == '1':
                    wood[str(turn)] += 1
                    current_profit[str(turn)] += wood_profit
            else:
                if not bought:
                    new_square = [x, y_sur]
                    if new_square!=goal:
                        list_property, current_profit, wood, cash, bought, recursed_map = buy_surrounding_goal(new_square, list_property, board_size, exploration_price, turn, current_profit, wood, list_color_map, bought, cash, recursed_map, n_paths)


    for x_sur in range(x-1, x+2):
        x_sur = min(x_sur, board_size[0]-1)
        x_sur = max(x_sur, 0)
        side_squared, _ = surrounded_property(x_sur, y, turn, list_property, board_size)
        key = str(x_sur) + str(y)

        if key not in recursed_map.keys():
            recursed_map[key] = n_paths
            n_paths += 1

            if side_squared and not bought and list_property[y][x_sur]=='0':
                bought = True
                list_property[y][x_sur] = str(turn)
                cash[str(turn)] -= exploration_price
                if list_color_map[y][x_sur] == '1':
                    wood[str(turn)] += 1
                    current_profit[str(turn)] += wood_profit
            else:
                if not bought:
                    new_square = [x_sur, y]
                    if new_square!=goal:
                        list_property, current_profit, wood, cash, bought, recursed_map = buy_surrounding_goal(new_square, list_property, board_size, exploration_price, 
                        turn, current_profit, wood, list_color_map, bought, cash, recursed_map, n_paths)

    return list_property, current_profit, wood, cash, bought, recursed_map


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
                list_property, current_profit, wood, cash, bought, recursed_map, _ = buy_surrounding_goal(goal, list_property, board_size, exploration_price, turn, 
                current_profit, wood, list_color_map, bought, cash, recursed_map = {}, n_paths=0)
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