# pygame version: 2.0.1
#python version 3.8.3
import pygame, sys
import random
import json

from general_use import surrounded_property, draw_text_centered, draw_text_top_left, conf_menu, create_buttons
from draw import draw_top_side, draw_leyend, draw_map
from AI import get_possible_square, movement_IA 

window_x = 500
window_y = 500

clock = pygame.time.Clock()
pygame.font.init()

screen = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption("Juego")

square_size = 40
board_size = [8, 8]

wood_color = (128, 64, 0)
factory_color = (120, 120, 120)
nothing_color = (200,200,200)

black = (0, 0, 0)
color_player1 = (200, 0, 0)
color_player2 = (0, 200, 0)
goal_color = (0, 0, 200)

dict_square_col = {'0': nothing_color, '1': wood_color, '2': factory_color}
dict_prop_col = {'0': black, '1': color_player1, '2': color_player2, '3': goal_color}

font = pygame.font.SysFont(None, 40)
coord_buttons = [(100, 120, 300, 80), (100, 250, 300, 80)]
button_color = (128, 64, 0)
background_main_menu_color = (200,150,100)
button_function = ["main_loop(True,", "main_loop(False,"]

spanish_button = ["vs IA", "2 jugadores"]
english_button = ["vs AI", "2 players"]


with open('parameters.txt', 'r') as outfile:
    data = json.load(outfile)

factory_price = data['factory_price']
exploration_price = data['exploration_price']
wood_profit = data['wood_profit']
factory_profit = data['factory_profit']
initial_cash = data['initial_cash']
goal_price = data['goal_price']

def end(turn, winner, window_x, window_y, screen, ia, language):
    if language == 'Spanish':
        if ia:
            if str(turn) == '2':
                lostTxt = 'La IA pierde. No puede pagar. A regañar a la programadora...'
                winTxt = 'Te ha ganado la IA. A seguir practicando'
        if not ia or str(turn)!='2':
            lostTxt = 'Jugador' + str(turn) + ' pierde! No tenía oro para pagar los impuestos...'
            winTxt ='Jugador' + str(turn) + ' gana! Enhorabuena!'
    if language == 'English':
        if ia:
            if str(turn) == '2':
                lostTxt = 'AI lost. It can\'t pay the taxes...'
                winTxt = 'AI won.'
        if not ia or str(turn)!='2':
            lostTxt = 'Player' + str(turn) + ' lost!'
            winTxt ='Player' + str(turn) + ' win! Congratulations!'
    lost_font = pygame.font.SysFont(None, 25)
    again_font = pygame.font.SysFont(None, 25)
    screen.fill((0, 0, 0))

    if winner:
        label = lost_font.render(winTxt, 1, (255,255,255))
    else:
        label = lost_font.render(lostTxt, 1, (255,255,255))

    screen.blit(label, (window_x / 2 - label.get_width() / 2, window_y / 2 - label.get_height() / 2))
    pygame.display.update()

    pygame.time.delay(2000)

    run = True
    while run:
        screen.fill((0,0,0))
        if language == 'Spanish':
            text = 'Pulsa cualquier tecla para volver a jugar'
        elif language == 'English':
            text = 'Press any key to play again'
        label = again_font.render(text, 1, (255,255,255))
        screen.blit(label, (window_x / 2 - label.get_width() / 2, window_y / 2 - label.get_height() / 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                run = False
    main_loop(ia, language)


def create_map(square_size, board_size, window_x, window_y):
    space_between_squares = 3
    n_divisions = 4
    wood_squares = []
    for i in range(n_divisions):
        wood_squares += random.sample(range(int(board_size[0]*board_size[1]/n_divisions*i +1), int(board_size[0]*board_size[1]/n_divisions*(i+1))), int(board_size[0]*board_size[1]/2/n_divisions))
    list_map = []
    list_rect_map = []
    list_property = []
    for y in range(board_size[1]):
        list_map_x = []
        list_rect_map_x = []
        list_property_x = []
        left_top_y = window_y - board_size[1] * (square_size+space_between_squares) - window_x/100
        for x in range(board_size[0]):
            if (board_size[0] * y + x + 1) in wood_squares:
                list_map_x += ['1']
            else:
                list_map_x +=['0']
            list_rect_map_x += [pygame.Rect(window_x/100 + space_between_squares + x * square_size + space_between_squares * x,
             left_top_y + y * square_size + space_between_squares * y, square_size, square_size)]
            list_property_x += ['0']
        list_map += [list_map_x]
        list_rect_map += [list_rect_map_x]
        list_property += [list_property_x]
    return list_map, list_rect_map, list_property, left_top_y


def first_position(board_size):
    first_x = random.randint(0, board_size[0]-1)
    first_y = random.randint(0, board_size[1]-1)
    return first_x, first_y


def main_loop(ia, language):
    list_color_map, list_rect_map, list_property, left_top_y = create_map(square_size, board_size, window_x, window_y)
    run = True
    n_turns = 1
    goal_enclosed = False

    wood = {'1':0, '2': 0}
    factory = {'1':0, '2': 0}
    cash = {'1':initial_cash, '2': initial_cash}
    current_profit = {'1':0, '2': 0}

    first_turn = random.randint(1,2)
    turn = first_turn
    n_factory = 0
    taxes = int((0+2) * 1/2)

    not_end = True
    while not_end:
        first_x1, first_y1 = first_position(board_size)
        if list_color_map[first_y1][first_x1]=='0':
            not_end = False
    list_property[first_y1][first_x1] = '1'

    not_end = True
    while not_end:
        first_x2, first_y2 = first_position(board_size)
        if list_color_map[first_y2][first_x2]=='0' and first_y2!=first_y1 and first_x2!=first_x1:
            not_end = False
    list_property[first_y2][first_x2] = '2'

    n = 0
    equal = True
    goal_y = int((first_y2+first_y1)/2) + random.randint(0,1)
    goal_x = int((first_x2+first_x1)/2) + random.randint(0,1)
    step = 1
    while equal:
        if ([goal_x, goal_y]!=[first_x2, first_y2]) and ([goal_x, goal_y]!=[first_x1, first_y1]):
            equal = False
        else:
            if n%2==0:
                goal_x += step
                if goal_x > board_size[0]:
                    goal_x -= 2
                    step = -1
            if n%2==1:
                goal_y += 1
                if goal_y > board_size[1]:
                    goal_y -= 2
                    step = -1
        n += 1

    list_property[goal_y][goal_x] = '3'
    goal = [goal_x, goal_y]

    possible_squares, direction = get_possible_square(list_property, list_color_map, board_size, turn)

    sb_end = False
    while run:
        screen.fill((50, 50, 50))
        clock.tick(30)
        action = 0
        click = False
        #goal_enclosed = calculate_goal_enclosed(goal, board_size, list_property)
        draw_map(screen, list_color_map, list_rect_map, list_property, dict_square_col,  dict_prop_col, board_size, goal)
        draw_top_side(screen, left_top_y, wood, factory, cash, current_profit, turn, n_turns, window_x, taxes, language)
        draw_leyend(screen, wood_color, factory_color,  color_player1, color_player2, left_top_y, board_size, square_size, goal_color, language)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit() 
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        if ia:
            list_property, action, current_profit, wood, factory, list_color_map, sb_end, goal_enclosed  = movement_IA(possible_squares, list_property, list_color_map,
             board_size, turn, cash, goal_price, n_turns, current_profit, factory_price, exploration_price, goal, wood_profit, factory_profit, factory, wood, goal_enclosed)
        mx, my = pygame.mouse.get_pos()
        for y in range(board_size[0]):
            for x in range(board_size[1]):
                if list_rect_map[y][x].collidepoint((mx, my)) and click:
                    if list_property[y][x] == '0':
                        sided_square, direction = surrounded_property(x, y, turn, list_property, board_size)
                        if sided_square:
                            #screenshot = pygame.display.get_surface()
                            if language == 'Spanish':
                                confirm, conf_pass = conf_menu(screen, mx, my, 'Explorar:  ' + str(exploration_price), window_x, window_y, language)
                            elif language == 'English':
                                confirm, conf_pass = conf_menu(screen, mx, my, 'Explore:  ' + str(exploration_price), window_x, window_y, language)
                            if confirm and cash[str(turn)]>=exploration_price:
                                action += 1
                                list_property[y][x] = str(turn)
                                cash[str(turn)] -= exploration_price
                                if list_color_map[y][x] == '1':
                                    wood[str(turn)] += 1
                            if conf_pass:
                                action += 1
                    elif str(turn)==list_property[y][x] and list_color_map[y][x] != '2':
                        #screenshot = pygame.display.get_surface()
                        if language == 'Spanish':
                            confirm, conf_pass = conf_menu(screen, mx, my, 'Fábrica: ' + str(factory_price), window_x, window_y, language)
                        elif language == 'English':
                            confirm, conf_pass = conf_menu(screen, mx, my, 'Factory: ' + str(factory_price), window_x, window_y, language)
                        if confirm and cash[str(turn)]>=factory_price and n_factory==0:
                            action += 1
                            n_factory += 1
                            factory[str(turn)] += 1
                            cash[str(turn)] -= factory_price
                            if list_color_map[y][x] == '1':
                                wood[str(turn)] -= 1
                            list_color_map[y][x] = '2'
                        if conf_pass:
                            action += 1
                    elif list_property[y][x]=='3':
                        sided_square, direction = surrounded_property(x, y, turn, list_property, board_size)
                        if sided_square:
                            if language == 'Spanish':
                                confirm, conf_pass = conf_menu(screen, mx, my, 'Meta: ' + str(goal_price), window_x, window_y, language)
                            elif language == 'English':
                                confirm, conf_pass = conf_menu(screen, mx, my, 'Goal: ' + str(goal_price), window_x, window_y, language)
                            if confirm and cash[str(turn)] >= goal_price and factory[str(turn)]>4:
                                sb_end = True
                                run = False
                                action += 1
                                cash[str(turn)] -= goal_price
        if action == 1:
            current_profit[str(turn)] = wood_profit * wood[str(turn)] + factory_profit * factory[str(turn)]
            cash[str(turn)] += current_profit[str(turn)]
            if n_turns%2==0:
                for player_cash in cash:
                    cash[player_cash] -= taxes
                    if cash[player_cash] < 0:
                        end(int(player_cash), False, window_x, window_y, screen, ia, language)
                taxes = int((n_turns+2) * 1/2)
            if sb_end:
                run = False
                cash[str(turn)] -= taxes
                if cash[str(turn)] < 0:
                    winner = False
                else:
                    winner = True
                end(turn, winner, window_x, window_y, screen, ia, language)
            n_factory = 0
            turn = (n_turns+first_turn+1)%2 + 1
            n_turns += 1

        pygame.display.update()



def main_menu():
    run = True
    click = False
    languages = ['English', 'Spanish']
    language = languages[0]
    while True:
        screen.fill(background_main_menu_color)
        draw_text_centered('Main menu', font, (0, 0, 0), screen, 250, 50)
        click = False
        mx, my = pygame.mouse.get_pos()
        if language=='English':
            button_text = english_button
        if language == 'Spanish':
            button_text = spanish_button

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        n_button, click = create_buttons(coord_buttons, button_color, button_text, click, mx, my, screen, font)

        if click:
            function_name = button_function[n_button]
            eval(f'{function_name}"{language}")')

        font_lang = pygame.font.SysFont(None, 30)


        language_button = pygame.Rect((280, 420,200,60))
        
        pygame.draw.rect(screen, button_color, language_button)

        if click:
            if language_button.collidepoint((mx, my)):
                index = languages.index(language)
                new_index = index + 1
                if new_index > (len(languages) - 1):
                    new_index = 0
                language = languages[new_index]
        
        draw_text_centered('Language: ' + language, font_lang, (0, 0, 0), screen, 380, 450)

        pygame.display.update()
        clock.tick(30)

main_menu()