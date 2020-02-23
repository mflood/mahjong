import copy

class Discards():

    def __init__(self):
        self.tiles = []
        self.last_tile = None

    def __str__(self):
        return "{}".format(" ".join([str(x) for x in self.tiles]))

    def get_state(self):
        return (copy.copy(self.tiles), self.last_tile)

    def set_state(self, state):
        self.tiles = state[0]
        self.last_tile = state[1]

    def pull(self, tile):
        
        pull = None
        new_tiles = []
        for t in self.tiles:
            if not pull and t == tile:
                pull = t
            else:
                new_tiles.append(t)
        self.tiles = new_tiles
        return pull

    def add(self, tile):
        self.tiles.append(tile)
        self.last_tile = tile


