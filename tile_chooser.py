import copy
from tile import Tile
from suit import Suit


class TileChooser():

    def __init__(self):
        self.tile = Tile(Suit.NONE)

    def get_tile(self):
        return copy.copy(self.tile)

    def set_tile_from_key(self, k):

        if k == 'd':
            # toggle dragon
            dragons = [Suit.GREEN_DRAGON, Suit.WHITE_DRAGON, Suit.RED_DRAGON]
            if self.tile.suit in dragons:
                location = dragons.index(self.tile.suit)
                location += 1
                location %= len(dragons)
            else:
                location = 0

            self.tile = Tile(dragons[location])

        elif k == 'w':
            # toggle wind
            winds = [Suit.NORTH_WIND, Suit.SOUTH_WIND, Suit.EAST_WIND, Suit.WEST_WIND]
            if self.tile.suit in winds:
                location = winds.index(self.tile.suit)
                location += 1
                location %= len(winds)
            else:
                location = 0
            self.tile = Tile(winds[location])

        elif k == 'f':
            self.tile = Tile(Suit.FLOWER)
            
        else:
            try:
                normals = [Suit.BAM, Suit.CRAK, Suit.DOT]
                number = int(k)

                if number < 1 or number > 9:
                    return

                location = 0
                if self.tile.number == number:
                    if self.tile.suit in normals:
                        location = normals.index(self.tile.suit)
                        location += 1
                        location %= len(normals)
                    else:
                        location = 0

                self.tile = Tile(normals[location], number)

            except:
                return
                pass
