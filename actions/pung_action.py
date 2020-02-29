
from actions import GameAction
from actions import ActionException
from tile import Tile

class PungAction(GameAction):

    def __init__(self, wall, hand, discards):
        super().__init__()
        self.hand = hand
        self.wall = wall
        self.discards = discards

        # 0 = pung other
        # 1 = kong self
        # 2 = pung self
        # 3 = kong self
        self.mode = self.get_modes()[0]

        # for undo state
        self._wall_state = None
        self._hand_state = None
        self._discards_state = None

    def __str__(self):

        last_tile = self.discards.last_tile
        if self.mode == 0:
            return "Create pung from discard (other player): {}".format(last_tile.long_name())
        elif self.mode == 1:
            return "Create kong from discard (other player): {}".format(last_tile.long_name())
        elif self.mode == 2:
            return "Create pung from discard (my hand): {}".format(last_tile.long_name())
        elif self.mode == 3:
            return "Create kong from discard (my hand): {}".format(last_tile.long_name())
        else:
            return "Cannot pung / kong"

    def get_modes(self):
        
        if not self.discards.last_tile:
            return [4]

        modes = []

        wall_count = 0
        for t in self.wall.tiles:
            if t == self.discards.last_tile:
                wall_count += 1

        if wall_count > 1:
            # other pung
            modes.append(0)
        if wall_count > 2:
            # other kong
            modes.append(1)
            
        hand_count = 0
        for t in self.hand.tiles:
            if t == self.discards.last_tile:
                hand_count += 1

        if hand_count > 1:
            # self pung
            modes.append(2)
        if hand_count > 2:
            # self kong
            modes.append(3)

        if not modes:
            modes.append(4)

        return modes


    def toggle(self):
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

        if self.mode == 4:
            return

        if self.mode in [0, 1]:
            source = self.wall
        else:
            source = self.hand

        if self.mode in [0, 2]:
            # pung
            count = 3
        else:
            # kong
            count = 4

        last_tile = self.discards.last_tile

        if not last_tile:
            raise ActionException("discards has no last tile")

        if last_tile:
            for x in range(count - 1):
                t = source.pull(last_tile)
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
