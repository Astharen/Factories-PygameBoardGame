from abc import ABC, abstractmethod


class View(ABC):
    def __init__(self, screen, clock):
        self.presenter = None
        self.screen = screen
        self.clock = clock

    @abstractmethod
    def start(self):
        pass

    def set_presenter(self, presenter):
        self.presenter = presenter
