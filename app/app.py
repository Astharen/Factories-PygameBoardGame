import pygame

from data.constants import window_x, window_y
from helper.generic import instance_class_from_module_and_name, snake_to_camel_case


class App:

    def __init__(self):

        self.current_window = None
        self._presenter = None
        self.screen = None
        self.clock = None

    def start(self):
        self.screen = pygame.display.set_mode((window_x, window_y))
        self.clock = pygame.time.Clock()
        self.current_window = 'main_menu'
        self.set_window(self.current_window)

    def set_window(self, window_name, **model_kwargs):
        window_class_name = snake_to_camel_case(window_name)

        window_model = instance_class_from_module_and_name(f'models.{window_name}_model', window_class_name + 'Model')
        window_model.start(**model_kwargs)
        window_view = instance_class_from_module_and_name(f'views.{window_name}_view', window_class_name + 'View',
                                                          screen=self.screen, clock=self.clock)
        window_presenter = instance_class_from_module_and_name(f'presenters.{window_name}_presenter',
                                                               window_class_name + 'Presenter',
                                                               model=window_model, app=self)
        window_presenter.set_view(window_view)
        self.current_window = window_name
        window_view.main()
