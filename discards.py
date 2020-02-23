
class Discards():

    def __init__(self):
        self.tiles = []
        self.last_tile = None

    def __str__(self):
        return "{}".format(" ".join([str(x) for x in self.tiles]))

    def add(self, tile):
        self.tiles.append(tile)
        self.last_tile = tile


