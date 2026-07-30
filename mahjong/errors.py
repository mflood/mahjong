"""Every exception this package raises on purpose."""


class MahjongError(Exception):
    """Base class for all errors raised by this package."""


class InvalidTile(MahjongError):
    """A tile was constructed or parsed with impossible values."""


class InvalidHand(MahjongError):
    """A hand holds a number of tiles that no rule allows."""


class WallEmpty(MahjongError):
    """A tile was drawn from an exhausted wall."""


class TileNotPresent(MahjongError):
    """A tile was removed from a collection that does not hold it."""


class ActionNotAllowed(MahjongError):
    """A game action was attempted in a state that forbids it."""
