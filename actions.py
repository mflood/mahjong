



class GameAction():
    pass


class HandLastTileToDiscardAction(GameAction):

    def __init__(self, hand, discards):
        self.hand = hand
        self.discards = discards

        # for undo state
        self._hand_state = None
        self._discards_state = None

    def __str__(self):
        return "Discard from hand: {}".format(self.tile)

    def execute(self):

        self._hand_state = self.hand.get_state()
        self._discards_state = self.discards.get_state()

        last_tile = self.hand.last_tile
        if last_tile:
            if self.hand.pull(last_tile):
                self.discards.add(last_tile)

    def undo(self):
        self.hand.set_state(self._hand_state)
        self.discards.set_state(self._discards_state)

    def clone(self):
        None

class HandToDiscardAction(GameAction):

    def __init__(self, hand, discards, tile):
        self.hand = hand
        self.discards = discards
        self.tile = tile

        # for undo state
        self._hand_state = None
        self._discards_state = None

    def __str__(self):
        return "Discard from hand: {}".format(self.tile)

    def execute(self):

        self._hand_state = self.hand.get_state()
        self._discards_state = self.discards.get_state()

        if self.hand.pull(self.tile):
            self.discards.add(self.tile)

    def undo(self):
        self.hand.set_state(self._hand_state)
        self.discards.set_state(self._discards_state)

    def clone(self):
        return HandToDiscardAction(hand=self.hand,
                                   discards=self.discards,
                                   tile=self.tile)

class RandomFromWallToHandAction(GameAction):

    def __init__(self, wall, hand):
        self.wall = wall
        self.hand = hand

        # for undo state
        self._wall_state = None
        self._hands_state = None

    def __str__(self):
        return "Random Wall to Hand: {}".format(self.tile)

    def execute(self):

        self._wall_state = self.wall.get_state()
        self._hands_state = self.hand.get_state()

        tile = self.wall.draw()
        if tile:
            self.hand.add(tile)

    def undo(self):
        self.wall.set_state(self._wall_state)
        self.hand.set_state(self._hands_state)
    
    def clone(self):
        return None


class WallToHandAction(GameAction):

    def __init__(self, wall, hand, tile):
        self.wall = wall
        self.hand = hand
        self.tile = tile

        # for undo state
        self._wall_state = None
        self._hands_state = None

    def __str__(self):
        return "Wall to Hand: {}".format(self.tile)

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

