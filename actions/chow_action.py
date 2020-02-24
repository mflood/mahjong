
from actions import GameAction
from tile import Tile
from suit import Suit

class ChowAction(GameAction):

    def __init__(self, wall, hand, discards):
        self.hand = hand
        self.wall = wall
        self.discards = discards

        # 0 = chow x.. other
        # 1 = chow .x. other
        # 2 = chow ..x other
        # 3 = chow x.. self
        # 4 = chow .x. self
        # 5 = chow ..x self
        # 6 = impossible
        self.mode = self.get_modes()[0]

        # for undo state
        self._wall_state = None
        self._hand_state = None
        self._discards_state = None

    def __str__(self):

        last_tile = self.discards.last_tile
        tiles = self.get_tiles_for_mode(self.mode)
        if self.mode == 0:
            return "Chow x.. other player {} {} {}".format(*tiles)
        elif self.mode == 1:
            return "Chow .x. other player {} {} {}".format(*tiles)
        elif self.mode == 2:
            return "Chow ..x other player {} {} {}".format(*tiles)
        elif self.mode == 3:
            return "Chow x.. self {} {} {}".format(*tiles)
        elif self.mode == 4:
            return "Chow .x. self {} {} {}".format(*tiles)
        elif self.mode == 5:
            return "Chow ..x self {} {} {}".format(*tiles)
        else:
            return "Cannot chow"

    def get_tiles_for_mode(self, mode):
        
        last_tile = self.discards.last_tile
        if not last_tile:
            return (None, None, None)

        if mode in [0, 3]:
            return (
                last_tile,
                Tile(last_tile.suit, last_tile.number + 1),
                Tile(last_tile.suit, last_tile.number + 2),
            )
        elif mode in [1, 4]:
            return (
                Tile(last_tile.suit, last_tile.number - 1),
                last_tile,
                Tile(last_tile.suit, last_tile.number + 1),
            )
        elif mode in [2, 5]:
            return (
                Tile(last_tile.suit, last_tile.number - 2),
                Tile(last_tile.suit, last_tile.number - 1),
                last_tile,
            )


    def _find_neighbor(self, tile_list, tile, distance):
        """
            return true if neighbor exists
        """

        # edge cases
        #
        if tile.number + distance > 9:
            return False

        if tile.number + distance < 1:
            return False

        find_tile = Tile(tile.suit, tile.number + distance)
        for t in tile_list:
            if t == find_tile:
                return True

        return False

    def get_modes(self):
        
        if not self.discards.last_tile:
            return [6]

        if self.discards.last_tile.suit not in [Suit.BAM, Suit.CRAK, Suit.DOT]:
            return [6]

        modes = []

        wall_num_above = 0
        wall_num_below = 0

        if self._find_neighbor(self.wall.tiles, self.discards.last_tile, 1):
            wall_num_above = 1
            if self._find_neighbor(self.wall.tiles, self.discards.last_tile, 2):
                wall_num_above = 2
        if self._find_neighbor(self.wall.tiles, self.discards.last_tile, -1):
            wall_num_below = 1
            if self._find_neighbor(self.wall.tiles, self.discards.last_tile, -2):
                wall_num_below = 2

        if wall_num_above == 2:
            modes.append(0)
        if wall_num_above >= 1 and wall_num_below >= 1:
            modes.append(1)
        if wall_num_below == 2:
            modes.append(2)
            
        player_num_above = 0
        player_num_below = 0

        if self._find_neighbor(self.hand.tiles, self.discards.last_tile, 1):
            player_num_above = 1
            if self._find_neighbor(self.hand.tiles, self.discards.last_tile, 2):
                player_num_above = 2
        if self._find_neighbor(self.hand.tiles, self.discards.last_tile, -1):
            player_num_below = 1
            if self._find_neighbor(self.hand.tiles, self.discards.last_tile, -2):
                player_num_below = 2

        if player_num_above == 2:
            modes.append(3)
        if player_num_above >= 1 and player_num_below >= 1:
            modes.append(4)
        if player_num_below == 2:
            modes.append(5)
            

        if not modes:
            modes.append(6)

        return modes


    def toggle_mode(self):
        modes = self.get_modes()

        if self.mode in modes:

            location = modes.index(self.mode)
            location += 1
            location %= len(modes)
        else:
            raise Exception("Mode {} is not in {}".format(self.mode, modes))
            location = 0

        self.mode = modes[location]
        
    def execute(self):

        self._hand_state = self.hand.get_state()
        self._discards_state = self.discards.get_state()
        self._wall_state = self.wall.get_state()

        if self.mode == 6:
            return


        if self.mode in [0, 1, 2]:
            source = self.wall
        else:
            source = self.hand

        chow_tiles = self.get_tiles_for_mode(self.mode)

        last_tile = self.discards.last_tile

        if not last_tile:
            raise ActionException("discards has no last tile")

        for tile in chow_tiles:
            if tile == last_tile:
                continue
            t = source.pull(tile)
            if t:
                self.discards.add(t)
                self.discards.last_tile = None
            else:
                raise ActionException("could not pull {} from source {}".format(last_tile, type(source)))


    def undo(self):
        self.hand.set_state(self._hand_state)
        self.discards.set_state(self._discards_state)
        self.wall.set_state(self._wall_state)

    def clone(self):
        None

