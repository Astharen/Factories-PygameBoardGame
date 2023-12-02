from abstract_classes.view import View
from views.game.board_view import BoardView


class GameView(View):

    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.board = BoardView()

    def start(self):
        pass
