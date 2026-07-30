"""Chinese/Hong Kong mahjong: hand solving, and a terminal table to explore it."""

from .actions import (
    ClaimChow,
    ClaimPung,
    DiscardFromWall,
    DiscardLastDrawn,
    DiscardTile,
    DrawFromWall,
    GameAction,
    TakeFromWall,
)
from .errors import (
    ActionNotAllowed,
    InvalidHand,
    InvalidTile,
    MahjongError,
    TileNotPresent,
    WallEmpty,
)
from .game import Game
from .hand import Discards, Hand
from .solver import (
    Decomposition,
    Meld,
    completions,
    decompose,
    is_winning_hand,
    winning_tiles,
)
from .tiles import Suit, Tile, format_hand, parse_hand
from .wall import Wall, full_set

__version__ = "1.0.0"

__all__ = [
    "ActionNotAllowed",
    "ClaimChow",
    "ClaimPung",
    "Decomposition",
    "Discards",
    "DiscardFromWall",
    "DiscardLastDrawn",
    "DiscardTile",
    "DrawFromWall",
    "Game",
    "GameAction",
    "Hand",
    "InvalidHand",
    "InvalidTile",
    "MahjongError",
    "Meld",
    "Suit",
    "TakeFromWall",
    "Tile",
    "TileNotPresent",
    "Wall",
    "WallEmpty",
    "completions",
    "decompose",
    "format_hand",
    "full_set",
    "is_winning_hand",
    "parse_hand",
    "winning_tiles",
]
