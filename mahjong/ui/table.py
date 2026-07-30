"""The curses table.

All this does is paint the lines :mod:`~mahjong.ui.render` produces and feed
keystrokes to :mod:`~mahjong.ui.keys`. There is no game logic here, which is
why nothing here needs a test that drives a terminal.
"""

import curses

from .keys import handle_key
from .render import help_lines, render


def draw(screen, game, message=""):
    screen.erase()
    height, width = screen.getmaxyx()

    row = 0
    for line in render(game):
        if row >= height - 1:
            break
        screen.addnstr(row, 0, line, width - 1)
        row += 1

    for line in help_lines():
        if row >= height - 1:
            break
        screen.addnstr(row, 0, line, width - 1)
        row += 1

    if message and height > 1:
        screen.addnstr(height - 1, 0, message[: width - 1], width - 1)

    screen.refresh()


def loop(screen, game):
    curses.curs_set(0)
    message = "space to draw, q to quit"
    while True:
        draw(screen, game, message)
        try:
            key = screen.getkey()
        except curses.error:
            continue
        should_quit, message = handle_key(game, key)
        if should_quit:
            return 0


def run(game):
    """Open the table. Returns a process exit code."""
    return curses.wrapper(loop, game)
