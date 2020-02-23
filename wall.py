import copy
import random
import enum
from suit import Suit
from tile import Tile

class Wall():

    def __init__(self):
        self.tiles = []

    def __str__(self):
        return "{}".format("\n".join([str(x) for x in self.tiles]))

    def __len__(self):
        return len(self.tiles)

    def get_state(self):
        return copy.copy(self.tiles)

    def set_state(self, state):
        self.tiles = state

    def load_tiles(self):
        self.tiles = []
        for suit in [Suit.BAM, Suit.DOT, Suit.CRAK]:
            for x in range(1, 10): 
                for i in range(4):
                    tile = Tile(suit=suit, number=x)
                    self.tiles.append(tile)
        for suit in [ Suit.NORTH_WIND, Suit.WEST_WIND, Suit.SOUTH_WIND, Suit.EAST_WIND, Suit.GREEN_DRAGON, Suit.RED_DRAGON, Suit.WHITE_DRAGON ]:
            for x in range(4):
                tile = Tile(suit=suit, number=None)
                self.tiles.append(tile)

        for x in range(8):
            tile = Tile(suit=Suit.FLOWER, number=None)
            self.tiles.append(tile)

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

    def draw(self):
        tile = self.tiles.pop()
        return tile

    def shuffle(self):
        random.shuffle(self.tiles)




