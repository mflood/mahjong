import sys
import copy
from suit import Suit
from itertools import permutations
from itertools import combinations
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


    def _get_tiles_of_suit(self, suit, tiles):
        return_tiles = []
        for t in tiles:
            if t.suit == suit:
                return_tiles.append(t)
        return return_tiles
        

    def get_tiles_of_suit(self, suit):
        return self._get_tiles_of_suit(suit, self.tiles)

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
            for x in range(1, 8):
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
                # print("{}potential set: {}".format(padding, str(test)))

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
        return self._is_mahjong(self.tiles) 

    def _is_mahjong(self, hand_tiles):
        
#        if len(hand_tiles) < 14:
#            return False

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
            tiles = self._get_tiles_of_suit(suit, hand_tiles)
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
            tiles = self._get_tiles_of_suit(suit, hand_tiles)
            if len(tiles) == 0:
                continue

            if len(tiles) % 3 == 0 or len(tiles) % 3 == 2:
                new_sets, new_pair = self.get_sets_pair(tiles)
                if new_pair:
                    if pair:
                        # print("False because there is already a designated pair from another suit")
                        return False
                    # print("Setting pair to %s" % new_pair)
                    pair = new_pair

                if new_sets:
                    # print("Appending {} with {}".format(str(sets), str(new_sets)))
                    # This seems to be working
                    sets.extend(new_sets)
                    # print("Now set is {}".format(str(sets)))

                if len(sets) > 3 and pair:
                    return (sets, pair)

        return False


    def tiles_needed(self, wall):
        if len(self.tiles) < 14:
            return self._tiles_needed(self.tiles, wall)
        return []

    def _tiles_needed(self, hand_tiles, wall):
        
        # a hand is not solvable if it has more than 5 suits
        unique_suits = list(set([tile.suit for tile in hand_tiles]))
        if len(unique_suits) > 5:
            return []

        return_tiles = []
        wall_tile_size = 14 - len(hand_tiles)
        wall_perms = combinations(wall.tiles, wall_tile_size)

        wall_perms_as_list = [list(x) for x in wall_perms]
        
        unique_wall_perms = set(map(tuple, wall_perms_as_list))

        #print("candidate length: {}".format(len(unique_wall_perms)))

        for item in unique_wall_perms:
            #print("Examining perm item: {}".format(str(item)))
            new_hand = hand_tiles + list(item)
            if self._is_mahjong(new_hand):
                return_tiles.append(item)

        #print("Combinations: {}".format("\n-".join([str( " ".join([str(a) for a in x ])    ) for x in wall_perms])))
        return return_tiles
        

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
    
        for x in range(8):
            wall.pull(Tile(Suit.FLOWER))

        for x in range(11):
            t = wall.draw()
            hand.add(t)

        print("hand: {}".format(str(hand)))
        solutions = hand.tiles_needed(wall)
        if solutions:
            for x in solutions:
                print(" solved with {}".format([str(a) for a in x]))

        is_m = hand.is_mahjong()
        if is_m:
            print("Mahjong!!!")
            print("Hand is %s" % hand)
            sets, pair = is_m
            print("valid: {} {}".format(sets, pair))
            for item in sets:
                print("SET: {}".format(" ".join([str(x) for x in item])))
            print("PAIR: {}".format(" ".join([str(x) for x in pair])))
