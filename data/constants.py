import json

import pygame

window_x = 500
window_y = 500

# ------------- Game constants -------------

square_size = 40
board_size = [8, 8]
space_between_squares = 3
n_divisions = 4

with open('data/color_mapping.txt', 'r') as outfile:
    color_mapping = json.load(outfile)

# ------------- Main Menu constants -------------

pygame.font.init()
font = pygame.font.SysFont(None, 40)
coord_buttons = [(100, 120, 300, 80), (100, 250, 300, 80)]

button_function = ["main_loop(True,", "main_loop(False,"]

button_text_all_lang = {'English': ["vs AI", "2 players"], 'Spanish': ["vs IA", "2 jugadores"]}
legend_color_text_mapping = {'language': {'English': ['Wood', 'Factory', 'Goal', 'Player 1', 'Player 2'],
                                          'Spanish': ['Madera', 'Fábrica', 'Meta', 'Jugador 1', 'Jugador 2']},
                             'color': [color_mapping['wood'], color_mapping['factory'], color_mapping['goal'],
                                       color_mapping['player1'], color_mapping['player2']],
                             'border': [None, None, None, 2, 2]}
