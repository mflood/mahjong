"""Command line: ``solve``, ``waiting``, ``deal`` and ``play``.

The first three are headless and pure, which is what makes the solver easy to
demonstrate and to test. ``play`` opens the curses table.
"""

import argparse
import json
import sys

from .errors import MahjongError
from .game import Game
from .solver import (
    WINNING_HAND_SIZE,
    completions,
    decompose,
    is_winning_hand,
    winning_tiles,
)
from .tiles import format_hand, parse_hand
from .wall import Wall


def build_parser():
    parser = argparse.ArgumentParser(
        prog="mahjong",
        description="Solve and explore Chinese/Hong Kong mahjong hands.",
        epilog="Tiles are written B1-B9 bamboo, C1-C9 characters, D1-D9 dots, "
        "WE/WS/WW/WN winds, DG/DR/DW dragons, FL flower.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    solve = subparsers.add_parser("solve", help="is this hand a winner?")
    solve.add_argument("tiles", nargs="+", help="tile codes, e.g. B1 B2 B3 ...")
    solve.add_argument("--json", action="store_true", help="machine-readable output")
    solve.set_defaults(handler=command_solve)

    waiting = subparsers.add_parser(
        "waiting", help="which tiles would complete this hand?"
    )
    waiting.add_argument("tiles", nargs="+", help="tile codes")
    waiting.add_argument("--json", action="store_true")
    waiting.set_defaults(handler=command_waiting)

    deal = subparsers.add_parser("deal", help="deal a random hand")
    deal.add_argument("--count", type=int, default=13, help="tiles to deal")
    deal.add_argument("--seed", type=int, help="make the deal reproducible")
    deal.add_argument("--json", action="store_true")
    deal.set_defaults(handler=command_deal)

    play = subparsers.add_parser("play", help="open the interactive table")
    play.add_argument("--seed", type=int, help="make the deal reproducible")
    play.set_defaults(handler=command_play)

    return parser


def command_solve(args):
    tiles = parse_hand(" ".join(args.tiles))
    result = decompose(tiles)
    winning = is_winning_hand(tiles)

    if args.json:
        print(
            json.dumps(
                {
                    "hand": format_hand(tiles),
                    "tile_count": len(tiles),
                    "winning": winning,
                    "melds": [
                        {"kind": m.kind, "tiles": [t.code for t in m.tiles]}
                        for m in (result.melds if result else ())
                    ],
                    "pair": [t.code for t in result.pair] if result else None,
                },
                indent=2,
            )
        )
        return 0 if winning else 1

    print("hand:  %s  (%d tiles)" % (format_hand(tiles), len(tiles)))
    if winning:
        print("result: winning hand")
    elif result:
        print(
            "result: not a winning hand — decomposes, but into %d melds, not %d"
            % (len(result.melds), WINNING_HAND_SIZE // 3)
        )
    else:
        print("result: not a winning hand — no decomposition into melds and a pair")

    if result:
        for meld in result.melds:
            print("  %-4s %s" % (meld.kind, meld))
        print("  pair %s %s" % (result.pair[0].code, result.pair[1].code))
    return 0 if winning else 1


def command_waiting(args):
    tiles = parse_hand(" ".join(args.tiles))
    missing = WINNING_HAND_SIZE - len(tiles)

    if missing == 1:
        found = [(t,) for t in winning_tiles(tiles)]
    else:
        found = completions(tiles)

    if args.json:
        print(
            json.dumps(
                {
                    "hand": format_hand(tiles),
                    "tiles_missing": missing,
                    "completions": [[t.code for t in combo] for combo in found],
                },
                indent=2,
            )
        )
        return 0 if found else 1

    print("hand: %s  (%d tiles, %d missing)" % (format_hand(tiles), len(tiles), missing))
    if not found:
        print("nothing completes this hand")
        return 1
    print("completed by:")
    for combo in found:
        print("  %s" % " ".join(t.code for t in combo))
    return 0


def command_deal(args):
    wall = Wall(seed=args.seed).shuffle()
    tiles = wall.deal(args.count)

    if args.json:
        print(
            json.dumps(
                {"hand": format_hand(tiles), "tiles": [t.code for t in sorted(tiles)]},
                indent=2,
            )
        )
        return 0

    print(format_hand(tiles))
    return 0


def command_play(args):
    try:
        from .ui.table import run
    except ImportError as exc:  # pragma: no cover - curses is stdlib on posix
        print("error: could not start the table: %s" % (exc,), file=sys.stderr)
        return 1
    return run(Game(seed=args.seed))


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.handler(args)
    except MahjongError as exc:
        print("error: %s" % (exc,), file=sys.stderr)
        return 2
