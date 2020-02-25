from actions import GameAction

class WallToHandAction(GameAction):

    def __init__(self, wall, hand, tile):
        self.wall = wall
        self.hand = hand
        self.tile = tile

        # for undo state
        self._wall_state = None
        self._hands_state = None

    def __str__(self):
        return "Wall to Hand: {}".format(self.tile.long_name())

    def execute(self):

        self._wall_state = self.wall.get_state()
        self._hands_state = self.hand.get_state()

        if self.wall.pull(self.tile):
            self.hand.add(self.tile)

    def undo(self):
        self.wall.set_state(self._wall_state)
        self.hand.set_state(self._hands_state)

    def clone(self):
        return WallToHandAction(wall=self.wall,
                                hand=self.hand,
                                tile=self.tile)
