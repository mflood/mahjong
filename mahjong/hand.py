"""A player's hand, and the discard pile."""

from collections import Counter

from .errors import TileNotPresent
from .solver import decompose, is_winning_hand, winning_tiles
from .tiles import format_hand


class TilePile:
    """A sorted, mutable collection of tiles. Base for hands and discards."""

    def __init__(self, tiles=()):
        self._tiles = sorted(tiles)
        self.last_tile = self._tiles[-1] if self._tiles else None

    def __len__(self):
        return len(self._tiles)

    def __iter__(self):
        return iter(self._tiles)

    def __contains__(self, tile):
        return tile in self._tiles

    def __bool__(self):
        return bool(self._tiles)

    @property
    def tiles(self):
        return tuple(self._tiles)

    def add(self, tile):
        self._tiles.append(tile)
        self._tiles.sort()
        self.last_tile = tile
        return tile

    def remove(self, tile):
        try:
            self._tiles.remove(tile)
        except ValueError:
            raise TileNotPresent("no %s here" % tile.code) from None
        if self.last_tile == tile and tile not in self._tiles:
            self.last_tile = self._tiles[-1] if self._tiles else None
        return tile

    def counts(self):
        return Counter(self._tiles)

    def state(self):
        """A snapshot that :meth:`restore` can put back. Used for undo."""
        return (tuple(self._tiles), self.last_tile)

    def restore(self, state):
        self._tiles = list(state[0])
        self.last_tile = state[1]

    def __str__(self):
        return format_hand(self._tiles)


class Discards(TilePile):
    """Tiles nobody wants any more."""


class Hand(TilePile):
    """The tiles a player holds.

    Flowers are held separately: they score but never form part of a hand, so
    keeping them out of the concealed tiles means the solver never has to
    think about them.
    """

    def __init__(self, tiles=()):
        super().__init__(t for t in tiles if not t.is_bonus)
        self.flowers = sorted(t for t in tiles if t.is_bonus)

    def add(self, tile):
        if tile.is_bonus:
            self.flowers.append(tile)
            self.last_tile = tile
            return tile
        return super().add(tile)

    @property
    def concealed(self):
        """The tiles that count towards a winning hand."""
        return self.tiles

    def is_winning(self):
        return is_winning_hand(self._tiles)

    def decomposition(self):
        """How the hand breaks into melds and a pair, or None."""
        return decompose(self._tiles)

    def waiting_on(self, available=None):
        """Tiles that would complete this hand if drawn next."""
        return winning_tiles(self._tiles, available)

    def state(self):
        return (tuple(self._tiles), self.last_tile, tuple(self.flowers))

    def restore(self, state):
        self._tiles = list(state[0])
        self.last_tile = state[1]
        self.flowers = list(state[2])
