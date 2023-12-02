class Player:
    def __init__(self, name):
        self.name = name
        self.owned_tiles = []
        self.wood = None
        self.factory = None
        self.cash = None
        self.current_profit = None

    def start(self, initial_tile, cash):
        self.owned_tiles.append(initial_tile)
        self.cash = cash
        self.wood = 0
        self.factory = 0
        self.current_profit = 0
