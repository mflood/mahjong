from actions import GameAction

class WallToHandAction(GameAction):

    def __init__(self, wall, hand, tile_chooser):
        super().__init__()
        self.wall = wall
        self.hand = hand
        self._tile_chooser = tile_chooser

        # for undo state
        self._wall_state = None
        self._hands_state = None

    def __str__(self):
        return "Wall to Hand: {}".format(self._tile_chooser.get_tile().long_name())

    def execute(self):

        self._wall_state = self.wall.get_state()
        self._hands_state = self.hand.get_state()

        if self.wall.pull(self._tile_chooser.get_tile()):
            self.hand.add(self._tile_chooser.get_tile())

    def undo(self):
        self.wall.set_state(self._wall_state)
        self.hand.set_state(self._hands_state)

    def clone(self):
        return WallToHandAction(wall=self.wall,
                                hand=self.hand,
                                tile_chooser=self._tile_chooser)
