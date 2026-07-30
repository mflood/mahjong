"""Turning game state into lines of text.

Pure functions, no curses. The table module paints what these return, which
means the entire display can be checked in tests without a terminal.
"""

from ..solver import WINNING_HAND_SIZE
from ..tiles import format_hand

TILES_PER_ROW = 18


def tile_rows(tiles, per_row=TILES_PER_ROW):
    """Wrap tile codes into fixed-width rows."""
    codes = [t.code for t in tiles]
    if not codes:
        return ["(none)"]
    return [
        " ".join(codes[i : i + per_row]) for i in range(0, len(codes), per_row)
    ]


def hand_lines(game):
    """The player's tiles, melds and flowers."""
    lines = list(tile_rows(game.hand.tiles))
    if game.melds:
        lines.append("melds: " + "  ".join(format_hand(m) for m in game.melds))
    if game.hand.flowers:
        lines.append("flowers: %d" % len(game.hand.flowers))
    return lines


def analysis_lines(game):
    """What the solver makes of the hand right now."""
    lines = []
    lines.append("%d of %d tiles" % (len(game.all_tiles), WINNING_HAND_SIZE))

    if game.is_winning():
        lines.append("MAHJONG")
        result = game.decomposition()
        if result:
            for meld in result.melds:
                lines.append("  %-4s %s" % (meld.kind, meld))
            lines.append("  pair %s" % format_hand(result.pair))
        return lines

    waiting = game.waiting_on()
    if waiting:
        lines.append("waiting on: %s" % " ".join(t.code for t in waiting))
    else:
        result = game.decomposition()
        if result:
            lines.append(
                "partial: %d meld%s + pair"
                % (len(result.melds), "" if len(result.melds) == 1 else "s")
            )
        else:
            lines.append("no completion from the remaining wall")
    return lines


def status_line(game):
    return "wall %d   discards %d   %s" % (
        len(game.wall),
        len(game.discards),
        "undo available" if game.can_undo else "nothing to undo",
    )


def discard_lines(game):
    return tile_rows(game.discards.tiles)


def help_lines():
    return [
        "space  draw a tile from the wall",
        "b      burn a wall tile to the discards",
        "d      discard the tile you just drew",
        "p      claim the last discard as a pung",
        "c      claim the last discard as a chow",
        "u      undo",
        "q      quit",
    ]


def render(game):
    """The whole screen as a list of lines, panel by panel."""
    sections = [
        ("HAND", hand_lines(game)),
        ("ANALYSIS", analysis_lines(game)),
        ("DISCARDS", discard_lines(game)),
    ]
    lines = []
    for title, body in sections:
        lines.append(title)
        lines.extend("  " + line for line in body)
        lines.append("")
    lines.append(status_line(game))
    return lines
