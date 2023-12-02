import sys

import pygame

from Scripts.general_use import draw_text_centered, create_buttons
from abstract_classes.view import View
from data.constants import button_text_all_lang, color_mapping, font, button_function, coord_buttons


class MainMenuView(View):

    def __init__(self, screen, clock):
        super().__init__()
        self.screen = screen
        self.clock = clock
        self.button_text = None
        self.language = None

    def start(self):
        language = self.presenter.get_language()
        self.button_text = button_text_all_lang[language]

    def change_button_text(self, language):
        self.button_text = button_text_all_lang[language]

    def main(self):
        while True:
            self.screen.fill(color_mapping['background_main_menu_color'])
            draw_text_centered('Main menu', font, (0, 0, 0), self.screen, 250, 50)
            click = False
            mx, my = pygame.mouse.get_pos()

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
            n_button, main_buttons_click = create_buttons(coord_buttons, color_mapping['button_color'],
                                                          self.button_text, click, mx, my, self.screen, font)

            if main_buttons_click:
                is_ia = n_button == 0
                self.presenter.change_to_game(is_ia)

            font_lang = pygame.font.SysFont(None, 30)

            language_button = pygame.Rect((280, 420, 200, 60))

            pygame.draw.rect(self.screen, color_mapping['button_color'], language_button)

            if click:
                if language_button.collidepoint((mx, my)):
                    self.presenter.set_next_language()

            draw_text_centered('Language: ' + self.presenter.get_language(), font_lang,
                               (0, 0, 0), self.screen, 380, 450)

            pygame.display.update()
            self.clock.tick(30)
