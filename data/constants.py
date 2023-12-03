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
