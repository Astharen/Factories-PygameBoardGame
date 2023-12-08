import sys

import pygame

from abstract_classes.view import View
from data.constants import window_x, window_y


class EndView(View):

    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.font = pygame.font.SysFont(None, 25)

    def start(self):
        self.screen.fill((0, 0, 0))
        text = self.presenter.get_ending_text()
        label = self.font.render(text, 1, (255, 255, 255))

        self.screen.blit(label, (window_x / 2 - label.get_width() / 2, window_y / 2 - label.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(2000)

    def main(self):
        language = self.presenter.get_language()

        if language == 'Spanish':
            text = 'Pulsa cualquier tecla para volver a jugar'
        elif language == 'English':
            text = 'Press any key to play again'

        run = True
        while run:
            self.screen.fill((0, 0, 0))
            label = self.font.render(text, 1, (255,255,255))
            self.screen.blit(label, (window_x / 2 - label.get_width() / 2, window_y / 2 - label.get_height() / 2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    run = False

        vs_ai = self.presenter.get_vs_ai()
        self.presenter.change_to_game(vs_ai)
