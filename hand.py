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
        normals = self.get_normals()
        honors = self.get_honors()
        flowers = self.get_flowers()

        n = "{}".format(" ".join([str(x) for x in normals]))
        h = "{}".format(" ".join([str(x) for x in honors]))
        f = "{}".format(" ".join([str(x) for x in flowers]))

        return "{}\n{}\n{}".format(n, h, f)


    def get_tiles_of_suit(self, suit):
        tiles = []
        for t in self.tiles:
            if t.suit == suit:
                tiles.append(t)
        return tiles

    def is_mahjong(self):
        
        pair = None
        sets = []
        for suit in [
            Suit.GREEN_DRAGON,
            Suit.WHITE_DRAGON,
            Suit.RED_DRAGON,
            Suit.EAST_WIND,
            Suit.WEST_WIND,
            Suit.NORTH_WIND,
            Suit.SOUTH_WIND,
        ]:
            tiles = self.get_tiles_of_suit(suit)
            if not tiles:
                continue

            if len(tiles) == 2:
                if pair:
                    return False
                pair = tiles
            elif len(tiles) == 3:
                sets.append(tiles)
            else:
                # length is 1 or 4
                return False

            if len(sets) == 4 and pair:
                return True

        print("Fell through")
        return False


    def hand_size(self):
        """
             return number of tiles without flowers
        """
        non_flowers = list(filter(lambda x: x.suit != Suit.FLOWER, self.tiles))
        return len(non_flowers)

    def get_normals(self):
        normal_suits = [Suit.BAM, Suit.CRAK, Suit.DOT]
        normals = list(filter(lambda x: x.suit in normal_suits, self.tiles))
        return normals
        
    def get_honors(self):
        normal_suits = [Suit.BAM, Suit.CRAK, Suit.DOT]
        honors = list(filter(lambda x: x.suit != Suit.FLOWER and x.suit not in normal_suits, self.tiles))
        return honors

    def get_flowers(self):
        flowers = list(filter(lambda x: x.suit == Suit.FLOWER, self.tiles))
        return flowers

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


    
