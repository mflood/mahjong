import copy
from suit import Suit
from itertools import permutations
from tile import Tile

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


    def is_valid_pair(self, tile_list):
        return tile_list[0] == tile_list[1]
            
    def is_valid_subset(self, tile_list):
        if tile_list[0] == tile_list[1] and tile_list[1] == tile_list[2]:
            return True

        if tile_list[0].number + 1 == tile_list[1].number and tile_list[1].number + 1 == tile_list[2].number:
            return True

        return False
            
    def get_sets_pair(self, tile_list, padding = ""):
        
        # print("{}get_sets_pair for {}".format(padding, str(tile_list)))
        padding = padding + " "
        suit = tile_list[0].suit

        valid_sets = []
        if len(tile_list) % 3 == 2:
            # find pairs
            for x in range(1, 9):
                t = Tile(suit, x)
                valid_sets.append([t, t])
        else:
            for x in range(1, 7):
                t1 = Tile(suit, x)
                t2 = Tile(suit, x+1)
                t3 = Tile(suit, x+2)
                valid_sets.append([t1, t2, t3])
            for x in range(1, 9):
                t = Tile(suit, x)
                valid_sets.append([t, t, t])
        
        for test in valid_sets:
            copy_list = copy.copy(tile_list)
            error = False
            for tile in test:
                try:
                    copy_list.remove(tile)
                except ValueError:
                    error = True
                    break 

            if not error:
                # print("{}potential {}".format(padding, str(test)))

                if len(copy_list) == 0:
                    if len(test) == 2:
                        # print("{}terminal: returning [], {}".format(padding, str(test)))
                        return [], test
                    else:
                        # print("{}terminal: returning [{}], None".format(padding, str(test)))
                        return [test], None

                child_sets, child_pair = self.get_sets_pair(copy_list, padding=padding + "  ")
                if child_sets:
                    if len(test) == 2:
                        # print("{}return this pair plus recursion {}, {}".format(padding, str(child_sets), str(test)))
                        return_set = (child_sets, test)
                        # print("{} PAIR returning {}".format(padding, str(return_set)))
                        return return_set
                    else:
                        # print("{}returning this set plus recursion [{} plus {}], None".format(padding, str(test), str(child_sets)))
                        return_set = ([test, *child_sets], None)
                        # print("{} SET returning: {}".format(padding, str(return_set)))
                        return return_set

        
        # print("{}nope".format(padding))
        return None, None

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
        
        for suit in [
            Suit.BAM,
            Suit.CRAK,
            Suit.DOT
        ]:
            tiles = self.get_tiles_of_suit(suit)
            if len(tiles) == 0:
                continue
            if len(tiles) % 3 == 0 or len(tiles) % 3 == 2:
                new_sets, new_pair = self.get_sets_pair(tiles)
                if new_pair:
                    if pair:
                        return False
                    pair = new_pair

                if new_sets:
                    # print("Appending {} with {}".format(str(sets), str(new_sets)))
                    # This seems to be working
                    sets.extend(new_sets)
                    # print("Now set is {}".format(str(sets)))

                if len(sets) > 3 and pair:
                    return (sets, pair)

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



if __name__ == "__main__":
    from wall import Wall 


    wall = Wall()
    for x in range(1000000):

        hand = Hand()
        wall.load_tiles()
        wall.shuffle()
    
        for x in range(14):
            t = wall.draw()
            hand.add(t)

        is_m = hand.is_mahjong()
        if is_m:
            print("Mahjong!!!")
            print("Hand is %s" % hand)
            sets, pair = is_m
            print("valid: {} {}".format(sets, pair))
            for item in sets:
                print("SET: {}".format(" ".join([str(x) for x in item])))
            print("PAIR: {}".format(" ".join([str(x) for x in pair])))
