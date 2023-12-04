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

    def calc_wood_and_factory(self):
        self.wood = self.calc_num_owned_tile_type('wood')
        self.factory = self.calc_num_owned_tile_type('factory')

    def calc_num_owned_tile_type(self, tile_type):
        return sum([1 if tile.type == tile_type else 0 for tile in self.owned_tiles])
