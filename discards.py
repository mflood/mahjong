
class Discards():

    def __init__(self):
        self.tiles = []

    def __str__(self):
        return "{}".format(" ".join([str(x) for x in self.tiles]))

    def add(self, tile):
        self.tiles.append(tile)

    def last(self):
        return self.tiles[-1]
        

