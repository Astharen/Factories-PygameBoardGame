class TileView:

    def __init__(self, x, y):

        self.rect = pygame.Rect(window_x/100 + space_between_squares + x * square_size + space_between_squares * x,
             left_top_y + y * square_size + space_between_squares * y, square_size, square_size)