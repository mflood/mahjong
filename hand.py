import copy

class Hand():

    def __init__(self):
        self.tiles = []
        self.last_tile = None

    def __repr__(self):
        return "Hand REPR"

    def __str__(self):
        top = "{}".format(" ".join([str(x) for x in self.tiles]))
        return "{}\n{}".format(top)

    def get_state(self):
        return (copy.copy(self.tiles), self.last_tile)

    def set_state(self, state):
        self.tiles = state[0]
        self.last_tile = state[1]

    def add(self, tile):
        self.tiles.append(tile)
        self.last_tile = tile 

    def pull(self, tile):
        discarded = None
        new_tiles = []
        for t in self.tiles:
            if not discarded and t == tile:
                discarded = t
            else:
                new_tiles.append(t)
        self.tiles = new_tiles
        self.tiles.sort()
        self.last_tile = None 
        return discarded

