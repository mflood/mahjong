"""Mapping keystrokes to game actions.

Kept out of the curses module so the whole interaction model — which key does
what, and what happens when it is not allowed — can be tested by calling a
function with a string.
"""

from ..actions import (
    ClaimChow,
    ClaimPung,
    DiscardFromWall,
    DiscardLastDrawn,
    DrawFromWall,
)
from ..errors import MahjongError

QUIT_KEYS = ("q", "Q")
UNDO_KEYS = ("u", "U")

ACTION_KEYS = {
    " ": DrawFromWall,
    "b": DiscardFromWall,
    "d": DiscardLastDrawn,
    "p": ClaimPung,
    "c": ClaimChow,
}


def handle_key(game, key):
    """Apply `key` to `game`. Returns ``(should_quit, message)``.

    Never raises for an ordinary refusal — an action that is not currently
    allowed comes back as a message, because a table that crashes when you
    press pung at the wrong moment is not a table anyone can use.
    """
    if key in QUIT_KEYS:
        return True, "bye"

    if key in UNDO_KEYS:
        try:
            action = game.undo()
        except MahjongError as exc:
            return False, str(exc)
        return False, "undid %s" % action.name

    action_class = ACTION_KEYS.get(key.lower() if key != " " else key)
    if action_class is None:
        return False, ""

    action = action_class(game)
    if not action.is_allowed():
        return False, "cannot %s right now" % action.name

    try:
        game.perform(action)
    except MahjongError as exc:
        return False, str(exc)
    return False, action.name
