import pygame

from general_use import draw_text_centered, draw_text_top_left

def draw_top_side(screen, left_top_y, wood, factory, cash, current_profit, turn, n_turns, window_x, taxes, language):
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
        pygame.draw.rect(screen, (200, 200, 200), (20, 20,  x_table, y_table))
    elif language == 'English':
        text_list = english_text
        x_total_parts = 3 + 6 + 9 + 7 + 8# This has been calculated by counting the number of letter in each word and adding 2 (1 for each space) 
        # The words were: one number, wood, factory, money, profit
        x_player = int(x_table * 3 / x_total_parts)
        x_wood = int(x_table * 6 / x_total_parts)
        x_factory = int(x_table * 9 / x_total_parts)
        x_cash = int(x_table * 7 / x_total_parts)
        x_profit = int(x_table * 8 / x_total_parts)
        x_table = int(x_player + x_wood + x_factory + x_cash + x_profit)
        pygame.draw.rect(screen, (200, 200, 200), (20, 20,  x_table, y_table))
    x = 20
    # Player
    pygame.draw.rect(screen, (0, 0, 0), (x, 20, x_player, heigth_part), 2)
    pygame.draw.rect(screen, (0, 0, 0), (x, 20 + heigth_part, x_player, heigth_part), 2)
    draw_text_centered('1', font_conf, (0, 0, 0), screen, x + x_player/2, 20 + heigth_part + heigth_part/2)
    pygame.draw.rect(screen, (0, 0, 0), (x, 20 + 2*heigth_part, x_player, heigth_part), 2)
    draw_text_centered('2', font_conf, (0, 0, 0), screen, x + x_player/2, 20 + 2*heigth_part + heigth_part/2)
    x += x_player
    # Wood
    pygame.draw.rect(screen, (0, 0, 0), (x, 20, x_wood, heigth_part), 2)
    draw_text_centered(text_list[index], font_conf, (0, 0, 0), screen, x + x_wood/2, 20  + heigth_part/2)
    pygame.draw.rect(screen, (0, 0, 0), (x, 20 + heigth_part, x_wood, heigth_part), 2)
    draw_text_centered(str(wood['1']), font_conf, (0, 0, 0), screen, x + x_wood/2, 20 + heigth_part + heigth_part/2)
    pygame.draw.rect(screen, (0, 0, 0), (x, 20 + 2*heigth_part, x_wood, heigth_part), 2)
    draw_text_centered(str(wood['2']), font_conf, (0, 0, 0), screen, x + x_wood/2, 20 + 2*heigth_part + heigth_part/2)
    x += x_wood
    index += 1
    # F actory
    pygame.draw.rect(screen, (0, 0, 0), (x, 20, x_factory, heigth_part), 2)
    draw_text_centered(text_list[index], font_conf, (0, 0, 0), screen, x + x_factory/2, 20 + heigth_part/2)
    pygame.draw.rect(screen, (0, 0, 0), (x, 20 + heigth_part, x_factory, heigth_part), 2)
    draw_text_centered(str(factory['1']), font_conf, (0, 0, 0), screen, x + x_factory/2, 20 + heigth_part + heigth_part/2)
    pygame.draw.rect(screen, (0, 0, 0), (x, 20 + 2*heigth_part, x_factory, heigth_part), 2)
    draw_text_centered(str(factory['2']), font_conf, (0, 0, 0), screen, x + x_factory/2, 20 + 2*heigth_part + heigth_part/2)
    x += x_factory
    index += 1
    # Cash
    pygame.draw.rect(screen, (0, 0, 0), (x, 20, x_cash, heigth_part), 2)
    draw_text_centered(text_list[index], font_conf, (0, 0, 0), screen, x + x_cash/2, 20 + heigth_part/2)
    pygame.draw.rect(screen, (0, 0, 0), (x, 20 + heigth_part, x_cash, heigth_part), 2)
    draw_text_centered(str(cash['1']), font_conf, (0, 0, 0), screen, x + x_cash/2, 20 + heigth_part + heigth_part/2)
    pygame.draw.rect(screen, (0, 0, 0), (x, 20 + 2*heigth_part, x_cash, heigth_part), 2)
    draw_text_centered(str(cash['2']), font_conf, (0, 0, 0), screen, x + x_cash/2, 20 + 2*heigth_part + heigth_part/2)
    x += x_cash
    index += 1
    # Profit
    pygame.draw.rect(screen, (0, 0, 0), (x, 20, x_profit, heigth_part), 2)
    draw_text_centered(text_list[index], font_conf, (0, 0, 0), screen, x + x_profit/2, 20 + heigth_part/2)
    pygame.draw.rect(screen, (0, 0, 0), (x, 20 + heigth_part, x_profit, heigth_part), 2)
    draw_text_centered(str(current_profit['1']), font_conf, (0, 0, 0), screen, x + x_profit/2, 20 + heigth_part + heigth_part/2)
    pygame.draw.rect(screen, (0, 0, 0), (x, 20 + 2*heigth_part, x_profit, heigth_part), 2)
    draw_text_centered(str(current_profit['2']), font_conf, (0, 0, 0), screen, x + x_profit/2, 20 + 2*heigth_part + heigth_part/2)
    index += 1
    # Turns
    x_turn = x_table + 20 + 50
    draw_text_centered(text_list[index] + str(n_turns), font_conf, (255, 255, 255), screen, x_turn, 20)
    index += 1
    draw_text_centered(text_list[index], font_conf, (255, 255, 255), screen, x_turn, 60)
    index += 1
    draw_text_centered(text_list[index] + str(taxes), font_conf, (255, 255, 255), screen, x_turn, 100)


def draw_leyend(screen, wood_color, factory_color,  color_player1, color_player2, left_top_y, board_size, square_size, goal_color, language):
    left_x = int((square_size + 3) * board_size[0] + 30) 
    font_conf = pygame.font.SysFont(None, 20)
    y = left_top_y + 30
    spanish_text = ['Madera', 'Fábrica', 'Jugador 1', 'Jugador 2', 'Meta']
    english_text = ['Wood', 'Factory', 'Player 1', 'Player 2', 'Goal']
    index = 0

    if language == 'English':
        text_list = english_text
    elif language == 'Spanish':
        text_list = spanish_text

    # Resources
    draw_text_top_left(text_list[index], font_conf, (255, 255, 255), screen, left_x + 35, y)
    pygame.draw.rect(screen, wood_color, (left_x, y, 20, 20))
    y += 35
    index += 1
    draw_text_top_left(text_list[index], font_conf, (255, 255, 255), screen, left_x + 35, y)
    pygame.draw.rect(screen, factory_color, (left_x, y, 20, 20))
    y += 35
    index += 1
    draw_text_top_left(text_list[index], font_conf, (255, 255, 255), screen, left_x + 35, y)
    pygame.draw.rect(screen, color_player1, (left_x, y, 20, 20), 2)
    y +=35
    index += 1
    draw_text_top_left(text_list[index], font_conf, (255, 255, 255), screen, left_x + 35, y)
    pygame.draw.rect(screen, color_player2, (left_x, y, 20, 20), 2)
    y +=35
    index += 1
    draw_text_top_left(text_list[index], font_conf, (255, 255, 255), screen, left_x + 35, y)
    pygame.draw.rect(screen, goal_color, (left_x, y, 20, 20), 2)


def draw_map(screen, list_color_map, list_rect_map, list_property, dict_square_col,  dict_prop_col, board_size, goal):
    for y in range(board_size[1]):
        for x in range(board_size[0]):
            pygame.draw.rect(screen, dict_square_col[list_color_map[y][x]], list_rect_map[y][x])
            pygame.draw.rect(screen, dict_prop_col[list_property[y][x]], list_rect_map[y][x], 3)