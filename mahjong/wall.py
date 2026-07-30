"""The wall: all 144 tiles, shuffled, drawn from one end."""

import random
from collections import Counter

from .errors import TileNotPresent, WallEmpty
from .tiles import HONOUR_SUITS, MAX_RANK, MIN_RANK, NUMBERED_SUITS, Suit, Tile

COPIES_OF_EACH_TILE = 4
FLOWERS_IN_A_SET = 8
TILES_IN_A_SET = (
    len(NUMBERED_SUITS) * (MAX_RANK - MIN_RANK + 1) * COPIES_OF_EACH_TILE
    + len(HONOUR_SUITS) * COPIES_OF_EACH_TILE
    + FLOWERS_IN_A_SET
)


def full_set():
    """Every tile in a standard set: 108 numbered, 28 honours, 8 flowers."""
    tiles = []
    for suit in NUMBERED_SUITS:
        for rank in range(MIN_RANK, MAX_RANK + 1):
            tiles.extend(Tile(suit, rank) for _ in range(COPIES_OF_EACH_TILE))
    for suit in HONOUR_SUITS:
        tiles.extend(Tile(suit) for _ in range(COPIES_OF_EACH_TILE))
    tiles.extend(Tile(Suit.FLOWER) for _ in range(FLOWERS_IN_A_SET))
    return tiles


class Wall:
    """A shuffled stack of tiles. Draws come off the top."""

    def __init__(self, tiles=None, seed=None):
        self._tiles = list(tiles) if tiles is not None else full_set()
        self._random = random.Random(seed)

    def __len__(self):
        return len(self._tiles)

    def __iter__(self):
        return iter(self._tiles)

    def __bool__(self):
        return bool(self._tiles)

    @property
    def tiles(self):
        return tuple(self._tiles)

    def shuffle(self):
        """Shuffle in place. Seed the Wall to make this reproducible."""
        self._random.shuffle(self._tiles)
        return self

    def draw(self):
        if not self._tiles:
            raise WallEmpty("the wall is exhausted")
        return self._tiles.pop()

    def deal(self, count):
        """Draw `count` tiles at once."""
        return [self.draw() for _ in range(count)]

    def take(self, tile):
        """Remove a specific tile from anywhere in the wall.

        Used when setting up a known position rather than playing a real game.
        """
        try:
            self._tiles.remove(tile)
        except ValueError:
            raise TileNotPresent("the wall has no %s" % tile.code) from None
        return tile

    def set_tiles(self, tiles):
        """Replace the contents. Used to restore a snapshot for undo."""
        self._tiles = list(tiles)

    def counts(self):
        """How many of each tile remain, for use with the solver."""
        return Counter(self._tiles)

    def __repr__(self):
        return "Wall(%d tiles)" % len(self._tiles)
