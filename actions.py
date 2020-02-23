



class GameAction():
    pass


class WallToDiscardAction(GameAction):

    def __init__(self, wall, discards, tile):
        self.wall = wall
        self.discards = discards
        self.tile = tile

        # for undo state
        self._wall_state = None
        self._discards_state = None

    def __str__(self):
        return "Discard from wall: {}".format(self.tile)

    def execute(self):

        self._wall_state = self.wall.get_state()
        self._discards_state = self.discards.get_state()

        if self.wall.pull(self.tile):
            self.discards.add(self.tile)

    def undo(self):
        self.wall.set_state(self._wall_state)
        self.discards.set_state(self._discards_state)

    def clone(self):
        return WallToDiscardAction(wall=self.wall,
                                   discards=self.discards,
                                   tile=self.tile)

