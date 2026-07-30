"""Game actions, each of which knows how to undo itself.

Every action snapshots the game before it changes anything, so undo is a
restore rather than a hand-written inverse. That is the difference between
undo you can trust and undo that drifts out of sync with the forward path the
first time an action grows a second effect.
"""

from .errors import ActionNotAllowed
from .solver import TILES_IN_A_MELD
from .tiles import MAX_RANK, MIN_RANK, Tile


class GameAction:
    """Base class: snapshot, apply, restore."""

    name = "action"

    def __init__(self, game):
        self.game = game
        self._snapshot = None

    @property
    def performed(self):
        return self._snapshot is not None

    def is_allowed(self):
        """Whether the current game state permits this action."""
        return True

    def execute(self):
        if not self.is_allowed():
            raise ActionNotAllowed("%s is not allowed right now" % self.name)
        self._snapshot = self.game.snapshot()
        self._apply()
        return self

    def undo(self):
        if self._snapshot is None:
            raise ActionNotAllowed("%s has not been performed" % self.name)
        self.game.restore(self._snapshot)
        self._snapshot = None
        return self

    def _apply(self):
        raise NotImplementedError

    def __repr__(self):
        return "%s()" % type(self).__name__


class DrawFromWall(GameAction):
    """Take the next tile off the wall into the hand."""

    name = "draw"

    def is_allowed(self):
        return bool(self.game.wall)

    def _apply(self):
        self.game.hand.add(self.game.wall.draw())


class TakeFromWall(GameAction):
    """Take a named tile out of the wall into the hand.

    For setting up a position by hand rather than playing it out.
    """

    name = "take"

    def __init__(self, game, tile):
        super().__init__(game)
        self.tile = tile

    def is_allowed(self):
        return self.tile in self.game.wall.tiles

    def _apply(self):
        self.game.hand.add(self.game.wall.take(self.tile))


class DiscardTile(GameAction):
    """Move a chosen tile from the hand to the discard pile."""

    name = "discard"

    def __init__(self, game, tile):
        super().__init__(game)
        self.tile = tile

    def is_allowed(self):
        return self.tile in self.game.hand

    def _apply(self):
        self.game.discards.add(self.game.hand.remove(self.tile))


class DiscardLastDrawn(GameAction):
    """Throw away the tile just drawn."""

    name = "discard last"

    def is_allowed(self):
        last = self.game.hand.last_tile
        return last is not None and last in self.game.hand

    def _apply(self):
        last = self.game.hand.last_tile
        self.game.discards.add(self.game.hand.remove(last))


class DiscardFromWall(GameAction):
    """Burn the next wall tile straight to the discard pile.

    Stands in for the other three players taking their turns.
    """

    name = "burn"

    def is_allowed(self):
        return bool(self.game.wall)

    def _apply(self):
        self.game.discards.add(self.game.wall.draw())


class ClaimMeld(GameAction):
    """Take the last discard and complete a meld with tiles from the hand."""

    name = "claim"

    def __init__(self, game, tile=None):
        super().__init__(game)
        self.tile = tile if tile is not None else game.discards.last_tile

    def supporting_tiles(self):
        """The hand tiles that would join the claimed tile, or None."""
        raise NotImplementedError

    def is_allowed(self):
        if self.tile is None or self.tile not in self.game.discards:
            return False
        return self.supporting_tiles() is not None

    def _apply(self):
        support = self.supporting_tiles()
        self.game.discards.remove(self.tile)
        for tile in support:
            self.game.hand.remove(tile)
        self.game.melds.append(tuple(sorted(support + [self.tile])))


class ClaimPung(ClaimMeld):
    """Claim a discard to make three of a kind."""

    name = "pung"

    def supporting_tiles(self):
        held = [t for t in self.game.hand if t == self.tile]
        if len(held) < TILES_IN_A_MELD - 1:
            return None
        return held[: TILES_IN_A_MELD - 1]


class ClaimChow(ClaimMeld):
    """Claim a discard to make a run of three in one suit."""

    name = "chow"

    def supporting_tiles(self):
        """The two held tiles that would make a run with the claimed one.

        The claimed tile can sit at the bottom, middle or top of the run, so
        try each. Bounds are checked before building tiles, since a rank
        outside 1-9 is not a tile that can be constructed at all.
        """
        if self.tile is None or not self.tile.is_numbered:
            return None
        suit, rank = self.tile.suit, self.tile.rank
        held = self.game.hand.counts()

        for start in (rank - 2, rank - 1, rank):
            if start < MIN_RANK or start + TILES_IN_A_MELD - 1 > MAX_RANK:
                continue
            wanted = [
                Tile(suit, start + step)
                for step in range(TILES_IN_A_MELD)
                if start + step != rank
            ]
            if all(held.get(tile, 0) > 0 for tile in wanted):
                return wanted
        return None
