from actions import GameAction

class WallToDiscardAction(GameAction):

    def __init__(self, wall, discards, tile_chooser):
        super().__init__()
        self._wall = wall
        self._discards = discards
        self._tile_chooser = tile_chooser

        # for undo state
        self._wall_state = None
        self._discards_state = None

    def __str__(self):
        return "Discard from wall: {}".format(self._tile_chooser.get_tile().long_name())

    def execute(self):

        self._wall_state = self._wall.get_state()
        self._discards_state = self._discards.get_state()

        if self._wall.pull(self._tile_chooser.get_tile()):
            self._discards.add(self._tile_chooser.get_tile())

    def undo(self):
        self._wall.set_state(self._wall_state)
        self._discards.set_state(self._discards_state)

    def clone(self):
        return WallToDiscardAction(wall=self._wall,
                                   discards=self._discards,
                                   tile_chooser=self._tile_chooser)

