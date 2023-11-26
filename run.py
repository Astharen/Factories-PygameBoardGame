from models.game import Model
from modules.view import View
from presenters.presenter import Presenter
from modules.player import Player


if __name__ == '__main__':

    # Create instances and set up the MVP integration
    model = Model()
    view = View()
    presenter = Presenter(model)

    # Set the view reference in the presenter
    presenter.set_view(view)

    # Add players to the model
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    model.add_player(player1)
    model.add_player(player2)

    # Start the game and handle player movements through the presenter
    presenter.handle_player_movement(player1, (2, 3))
    presenter.handle_player_movement(player2, (5, 7))
