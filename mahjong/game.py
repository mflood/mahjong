"""Game state: a wall, a hand, a discard pile, and an undo history."""

from .errors import ActionNotAllowed
from .hand import Discards, Hand
from .solver import WINNING_HAND_SIZE, decompose, is_winning_hand, winning_tiles
from .wall import Wall

OPENING_HAND_SIZE = 13


class Game:
    """One player's view of a game, with every move reversible.

    There is no turn order and no opponents: this is a tool for exploring a
    hand — deal, draw, discard, claim, undo — not a four-player engine.
    """

    def __init__(self, wall=None, hand=None, discards=None, seed=None):
        self.wall = wall if wall is not None else Wall(seed=seed).shuffle()
        self.hand = hand if hand is not None else Hand()
        self.discards = discards if discards is not None else Discards()
        self.melds = []
        self.history = []

    def deal(self, count=OPENING_HAND_SIZE):
        """Draw an opening hand, replacing any flowers as they appear."""
        while len(self.hand) < count:
            tile = self.wall.draw()
            self.hand.add(tile)
        return self.hand

    def snapshot(self):
        return (
            self.wall.tiles,
            self.hand.state(),
            self.discards.state(),
            tuple(self.melds),
        )

    def restore(self, state):
        wall_tiles, hand_state, discard_state, melds = state
        self.wall.set_tiles(wall_tiles)
        self.hand.restore(hand_state)
        self.discards.restore(discard_state)
        self.melds = list(melds)

    def perform(self, action):
        """Run an action and record it so it can be undone."""
        action.execute()
        self.history.append(action)
        return action

    def undo(self):
        """Reverse the most recent action."""
        if not self.history:
            raise ActionNotAllowed("nothing to undo")
        action = self.history.pop()
        action.undo()
        return action

    @property
    def can_undo(self):
        return bool(self.history)

    @property
    def all_tiles(self):
        """Concealed tiles plus the tiles inside claimed melds.

        Claiming a pung moves three tiles out of the hand, so anything judging
        the hand as a whole has to look here rather than at the concealed
        tiles alone -- otherwise a hand can never be won after a claim.
        """
        melded = [tile for meld in self.melds for tile in meld]
        return list(self.hand.tiles) + melded

    @property
    def hand_is_full(self):
        """True once the hand holds a complete fourteen tiles."""
        return len(self.all_tiles) >= WINNING_HAND_SIZE

    def is_winning(self):
        return is_winning_hand(self.all_tiles)

    def decomposition(self):
        return decompose(self.all_tiles)

    def waiting_on(self):
        """Tiles that would complete the hand, limited to what is unseen."""
        return winning_tiles(self.all_tiles, self.wall.counts())
