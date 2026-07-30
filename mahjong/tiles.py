"""Suits, tiles, and the text notation used everywhere else.

Notation: a numbered tile is a suit letter followed by 1-9 (``B3``, ``C7``,
``D9``); an honour is two letters (``WE`` east wind, ``DG`` green dragon,
``FL`` flower). Nothing is ambiguous because the character after the suit
letter is a digit for numbered tiles and a letter for honours -- ``D9`` is
nine dots, ``DW`` is the white dragon.
"""

from dataclasses import dataclass
from enum import IntEnum

from .errors import InvalidTile

MIN_RANK = 1
MAX_RANK = 9


class Suit(IntEnum):
    BAMBOO = 1
    CHARACTER = 2
    DOT = 3

    EAST_WIND = 4
    SOUTH_WIND = 5
    WEST_WIND = 6
    NORTH_WIND = 7

    GREEN_DRAGON = 8
    RED_DRAGON = 9
    WHITE_DRAGON = 10

    FLOWER = 11

    @property
    def is_numbered(self):
        """Bamboo, characters and dots: the suits that run 1-9 and form runs."""
        return self in NUMBERED_SUITS

    @property
    def is_honour(self):
        """Winds and dragons: they pair and triple but never form a run."""
        return self in HONOUR_SUITS

    @property
    def is_bonus(self):
        """Flowers, which are set aside and never part of a hand."""
        return self is Suit.FLOWER


NUMBERED_SUITS = (Suit.BAMBOO, Suit.CHARACTER, Suit.DOT)
HONOUR_SUITS = (
    Suit.EAST_WIND,
    Suit.SOUTH_WIND,
    Suit.WEST_WIND,
    Suit.NORTH_WIND,
    Suit.GREEN_DRAGON,
    Suit.RED_DRAGON,
    Suit.WHITE_DRAGON,
)

SUIT_CODES = {Suit.BAMBOO: "B", Suit.CHARACTER: "C", Suit.DOT: "D"}
HONOUR_CODES = {
    "WE": Suit.EAST_WIND,
    "WS": Suit.SOUTH_WIND,
    "WW": Suit.WEST_WIND,
    "WN": Suit.NORTH_WIND,
    "DG": Suit.GREEN_DRAGON,
    "DR": Suit.RED_DRAGON,
    "DW": Suit.WHITE_DRAGON,
    "FL": Suit.FLOWER,
}
CODE_FOR_HONOUR = {suit: code for code, suit in HONOUR_CODES.items()}

LONG_NAMES = {
    Suit.BAMBOO: "Bamboo",
    Suit.CHARACTER: "Character",
    Suit.DOT: "Dot",
    Suit.EAST_WIND: "East Wind",
    Suit.SOUTH_WIND: "South Wind",
    Suit.WEST_WIND: "West Wind",
    Suit.NORTH_WIND: "North Wind",
    Suit.GREEN_DRAGON: "Green Dragon",
    Suit.RED_DRAGON: "Red Dragon",
    Suit.WHITE_DRAGON: "White Dragon",
    Suit.FLOWER: "Flower",
}


@dataclass(frozen=True, order=True)
class Tile:
    """One tile. Immutable and hashable, so tiles work as dict keys.

    Numbered tiles carry a rank of 1-9; honours and flowers carry None.
    """

    suit: Suit
    rank: int = None

    def __post_init__(self):
        if self.suit.is_numbered:
            if self.rank is None:
                raise InvalidTile("%s tiles need a rank" % LONG_NAMES[self.suit])
            if not MIN_RANK <= self.rank <= MAX_RANK:
                raise InvalidTile(
                    "rank %r is outside %d-%d" % (self.rank, MIN_RANK, MAX_RANK)
                )
        elif self.rank is not None:
            raise InvalidTile("%s tiles have no rank" % LONG_NAMES[self.suit])

    @property
    def is_numbered(self):
        return self.suit.is_numbered

    @property
    def is_honour(self):
        return self.suit.is_honour

    @property
    def is_bonus(self):
        return self.suit.is_bonus

    @property
    def code(self):
        """The text notation for this tile, e.g. ``B3`` or ``DG``."""
        if self.suit.is_numbered:
            return "%s%d" % (SUIT_CODES[self.suit], self.rank)
        return CODE_FOR_HONOUR[self.suit]

    @property
    def name(self):
        if self.suit.is_numbered:
            return "%d %s" % (self.rank, LONG_NAMES[self.suit])
        return LONG_NAMES[self.suit]

    def successor(self):
        """The next tile up in the same suit, or None if there isn't one."""
        if not self.suit.is_numbered or self.rank >= MAX_RANK:
            return None
        return Tile(self.suit, self.rank + 1)

    @classmethod
    def parse(cls, code):
        """Build a tile from its notation. Case-insensitive."""
        text = code.strip().upper()
        if len(text) != 2:
            raise InvalidTile("%r is not a tile code" % (code,))

        if text in HONOUR_CODES:
            return cls(HONOUR_CODES[text])

        letter, rest = text[0], text[1:]
        for suit, suit_code in SUIT_CODES.items():
            if letter == suit_code and rest.isdigit():
                return cls(suit, int(rest))
        raise InvalidTile("%r is not a tile code" % (code,))

    def __str__(self):
        return self.code


def parse_hand(text):
    """Parse a whitespace- or comma-separated list of tile codes.

    >>> [t.code for t in parse_hand("B1 B2 B3")]
    ['B1', 'B2', 'B3']
    """
    parts = [p for p in text.replace(",", " ").split() if p]
    return [Tile.parse(p) for p in parts]


def format_hand(tiles):
    """Render tiles back to notation, in sorted order."""
    return " ".join(t.code for t in sorted(tiles))


def all_tile_types():
    """Every distinct tile in the game, flowers excluded."""
    types = []
    for suit in NUMBERED_SUITS:
        types.extend(Tile(suit, rank) for rank in range(MIN_RANK, MAX_RANK + 1))
    types.extend(Tile(suit) for suit in HONOUR_SUITS)
    return types
