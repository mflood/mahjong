import copy
from suit import Suit

class Hand():

    def __init__(self):
        self.tiles = []
        self.last_tile = None

    def __repr__(self):
        return "Hand REPR"

    def __str__(self):
        normal_suits = [Suit.BAM, Suit.CRAK, Suit.DOT]
        normals = list(filter(lambda x: x.suit in normal_suits, self.tiles))
        honors = list(filter(lambda x: x.suit != Suit.FLOWER and x.suit not in normal_suits, self.tiles))
        flowers = list(filter(lambda x: x.suit == Suit.FLOWER, self.tiles))

        n = "{}".format(" ".join([str(x) for x in normals]))
        h = "{}".format(" ".join([str(x) for x in honors]))
        f = "{}".format(" ".join([str(x) for x in flowers]))

        return "{}\n{}\n{}".format(n, h, f)

    def get_state(self):
        return (copy.copy(self.tiles), self.last_tile)

    def set_state(self, state):
        self.tiles = state[0]
        self.last_tile = state[1]

    def add(self, tile):
        self.tiles.append(tile)
        self.tiles.sort()
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
        if self.tiles:
            self.last_tile = self.tiles[0]
        else:
            self.last_tile = None 
        return discarded

