class Player:
    def __init__(self, name):
        self.name = name
        self.owned_tiles = []
        self.wood = None
        self.factory = None
        self.cash = None
        self.current_profit = None

    def start(self, cash):
        self.cash = cash
        self.wood = 0
        self.factory = 0
        self.current_profit = 0

    def add_tile(self, tile):
        self.owned_tiles.append(tile)
