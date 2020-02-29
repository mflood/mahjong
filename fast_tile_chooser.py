import copy
from tile import Tile
from suit import Suit

suit_map = {
    'z': Suit.GREEN_DRAGON,
    'x': Suit.WHITE_DRAGON,
    'c': Suit.RED_DRAGON,

    'v': Suit.NORTH_WIND,
    'b': Suit.SOUTH_WIND,
    'n': Suit.EAST_WIND,
    'm': Suit.WEST_WIND,

    '0': Suit.FLOWER,
    
    '1': Suit.BAM,
    '2': Suit.BAM,
    '3': Suit.BAM,
    '4': Suit.BAM,
    '5': Suit.BAM,
    '6': Suit.BAM,
    '7': Suit.BAM,
    '8': Suit.BAM,
    '9': Suit.BAM,
    
    'q': Suit.CRAK,
    'w': Suit.CRAK,
    'e': Suit.CRAK,
    'r': Suit.CRAK,
    't': Suit.CRAK,
    'y': Suit.CRAK,
    'u': Suit.CRAK,
    'i': Suit.CRAK,
    'o': Suit.CRAK,
    
    'a': Suit.DOT,
    's': Suit.DOT,
    'd': Suit.DOT,
    'f': Suit.DOT,
    'g': Suit.DOT,
    'h': Suit.DOT,
    'j': Suit.DOT,
    'k': Suit.DOT,
    'l': Suit.DOT,
}


number_map = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    
    'q': 1,
    'w': 2,
    'e': 3,
    'r': 4,
    't': 5,
    'y': 6,
    'u': 7,
    'i': 8,
    'o': 9,
    
    'a': 1,
    's': 2,
    'd': 3,
    'f': 4,
    'g': 5,
    'h': 6,
    'j': 7,
    'k': 8,
    'l': 9,
}

class FastTileChooser():

    def __init__(self):
        self._tile = Tile(Suite.NONE)

    def get_tile(self):
        return copy.copy(self._tile)

    def set_tile_from_key(self, k):

        if suit = suit_map.get(k):
            self._tile.suit = suit
            
            number = numnber_map.get(k)
            self.number = number
# end
