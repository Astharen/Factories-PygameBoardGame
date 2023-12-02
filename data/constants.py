import json

import pygame

window_x = 500
window_y = 500

# ------------- Game constants -------------

square_size = 40
board_size = [8, 8]
space_between_squares = 3
n_divisions = 4

with open('color_mapping.txt', 'r') as outfile:
    color_mapping = json.load(outfile)

dict_square_col = {'0': color_mapping['nothing_color'], '1': color_mapping['wood_color'],
                   '2': color_mapping['factory_color']}
dict_prop_col = {'0': color_mapping['black'], '1': color_mapping['color_player1'],
                 '2': color_mapping['color_player2'], '3': color_mapping['goal_color']}

# ------------- Main Menu constants -------------

pygame.font.init()
font = pygame.font.SysFont(None, 40)
coord_buttons = [(100, 120, 300, 80), (100, 250, 300, 80)]

button_function = ["main_loop(True,", "main_loop(False,"]

button_text_all_lang = {'English': ["vs AI", "2 players"], 'Spanish': ["vs IA", "2 jugadores"]}
