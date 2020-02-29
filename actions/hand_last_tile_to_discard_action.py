from actions import GameAction

class HandLastTileToDiscardAction(GameAction):

    def __init__(self, hand, discards):
        super().__init__()
        self.hand = hand
        self.discards = discards

        # for undo state
        self._hand_state = None
        self._discards_state = None

    def __str__(self):
        return "Discard from hand: {}".format(self.tile.long_name())

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

