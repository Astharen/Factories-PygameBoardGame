from data.constants import board_size, window_x, window_y, square_size, space_between_squares


class BoardView:

    def __init__(self):
        self.left_top_y = window_y - board_size[1] * (square_size + space_between_squares) - window_x / 100
