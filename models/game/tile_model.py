class TileModel:

    def __init__(self, x, y, tile_type):
        self.x = x
        self.y = y
        self.type = tile_type
        self.owner = 'black'

    def set_owner(self, player):
        self.owner = player.name
