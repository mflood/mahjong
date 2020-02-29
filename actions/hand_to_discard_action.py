from actions import GameAction
import copy

class HandToDiscardAction(GameAction):

    def __init__(self, hand, discards, tile_chooser):
        super().__init__()
        self.hand = hand
        self.discards = discards
        self.tile = hand.last_tile
        self.tile_chooser = tile_chooser

        # for undo state
        self._hand_state = None
        self._discards_state = None

    def __str__(self):
        if self.tile:
            return "Discard from hand: {}".format(self.tile.long_name())
        else:
            return "Discard from hand: (no tile selected)"

    def execute(self):

        self._hand_state = self.hand.get_state()
        self._discards_state = self.discards.get_state()

        if self.hand.pull(self.tile):
            self.discards.add(self.tile)

    def toggle(self, reverse=False, tab=False):
        tiles = copy.copy(self.hand.tiles)
        tiles = list(set(tiles))
        tiles.sort()
        idx = 0
        if self.hand.last_tile:
            idx = tiles.index(self.hand.last_tile)
            if tab:
                # go to the next suit
                current_suit = self.hand.last_tile.suit
                loop_idx = None
                while loop_idx != idx:
                    # set first time through
                    if loop_idx is None:
                        loop_idx = idx
                    else:
                        tile = tiles[loop_idx]
                        if tile.suit != current_suit:
                            idx = loop_idx
                            break
                    loop_idx += 1
                    if loop_idx >= len(tiles):
                        loop_idx = 0
            else:
                if reverse:
                    idx -= 1
                    idx += len(tiles)
                else:
                    idx += 1
                idx %= len(tiles)

        new_last_tile = tiles[idx]
        self.hand.last_tile = new_last_tile
        self.tile = new_last_tile

    def undo(self):
        self.hand.set_state(self._hand_state)
        self.discards.set_state(self._discards_state)

    def clone(self):
        return HandToDiscardAction(hand=self.hand,
                                   discards=self.discards,
                                   tile=copy.copy(self.tile))

