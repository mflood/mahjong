"""Tests for the terminal layer.

The curses module itself is never imported here. Everything the interface
actually decides -- what to display, which key does what, what happens when an
action is refused -- lives in render.py and keys.py as plain functions, so it
is checked directly.
"""

from mahjong.game import Game
from mahjong.hand import Discards, Hand
from mahjong.tiles import Tile, parse_hand
from mahjong.ui.keys import ACTION_KEYS, handle_key
from mahjong.ui.render import (
    analysis_lines,
    discard_lines,
    hand_lines,
    help_lines,
    render,
    status_line,
    tile_rows,
)
from mahjong.wall import Wall


def game_with(hand="", wall="", discards=""):
    return Game(
        wall=Wall(tiles=parse_hand(wall)),
        hand=Hand(parse_hand(hand)),
        discards=Discards(parse_hand(discards)),
    )


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------


def test_tile_rows_wraps_long_hands():
    tiles = parse_hand(" ".join(["B1"] * 40))
    rows = tile_rows(tiles, per_row=18)

    assert len(rows) == 3
    assert rows[0].count("B1") == 18


def test_tile_rows_of_nothing_says_so():
    assert tile_rows([]) == ["(none)"]


def test_hand_lines_show_melds_and_flowers():
    game = game_with(hand="B1 B2 FL")
    game.melds.append(tuple(parse_hand("C1 C2 C3")))

    lines = "\n".join(hand_lines(game))

    assert "B1 B2" in lines
    assert "C1 C2 C3" in lines
    assert "flowers: 1" in lines


def test_analysis_announces_a_win():
    game = game_with(hand="B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6 D5 D5")
    lines = "\n".join(analysis_lines(game))

    assert "MAHJONG" in lines
    assert "pair D5 D5" in lines


def test_analysis_reports_what_the_hand_waits_on():
    game = game_with(
        hand="B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6 D5", wall="D5 D5 D5"
    )
    lines = "\n".join(analysis_lines(game))

    assert "waiting on: D5" in lines


def test_analysis_says_so_when_the_wall_cannot_help():
    game = game_with(hand="B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6 D5", wall="B7")
    lines = "\n".join(analysis_lines(game))

    assert "no completion" in lines


def test_analysis_counts_melds_towards_the_total():
    game = game_with(hand="B1 B2")
    game.melds.append(tuple(parse_hand("C1 C2 C3")))

    assert "5 of 14 tiles" in "\n".join(analysis_lines(game))


def test_status_line_reports_the_piles_and_undo():
    game = game_with(hand="B1", wall="C1 C2", discards="D1")

    assert "wall 2" in status_line(game)
    assert "discards 1" in status_line(game)
    assert "nothing to undo" in status_line(game)


def test_status_line_notices_when_undo_is_available():
    game = game_with(wall="C1")
    handle_key(game, " ")

    assert "undo available" in status_line(game)


def test_discard_lines_render_the_pile():
    game = game_with(discards="B1 C2")

    assert discard_lines(game) == ["B1 C2"]


def test_render_produces_every_panel():
    game = game_with(hand="B1", wall="C1", discards="D1")
    screen = "\n".join(render(game))

    for heading in ("HAND", "ANALYSIS", "DISCARDS"):
        assert heading in screen


def test_help_covers_every_bound_key():
    text = " ".join(help_lines())

    for key in ACTION_KEYS:
        label = "space" if key == " " else key
        assert label in text, "key %r is unbound in the help" % key
    assert "u " in text and "q " in text


# --------------------------------------------------------------------------
# Key handling
# --------------------------------------------------------------------------


def test_space_draws_a_tile():
    game = game_with(wall="B1")
    quit_now, message = handle_key(game, " ")

    assert not quit_now
    assert str(game.hand) == "B1"
    assert message == "draw"


def test_q_quits():
    quit_now, _ = handle_key(game_with(), "q")

    assert quit_now


def test_an_unbound_key_does_nothing():
    game = game_with(wall="B1")
    quit_now, message = handle_key(game, "z")

    assert not quit_now
    assert message == ""
    assert len(game.wall) == 1


def test_a_refused_action_reports_rather_than_raising():
    """Pressing pung at the wrong moment must not take the table down."""
    game = game_with(hand="B1")
    quit_now, message = handle_key(game, "p")

    assert not quit_now
    assert "cannot pung" in message


def test_drawing_from_an_empty_wall_reports_rather_than_raising():
    game = game_with()
    quit_now, message = handle_key(game, " ")

    assert not quit_now
    assert "cannot draw" in message


def test_u_undoes_the_last_action():
    game = game_with(wall="B1")
    handle_key(game, " ")
    _, message = handle_key(game, "u")

    assert len(game.hand) == 0
    assert "undid draw" in message


def test_undo_with_empty_history_reports_rather_than_raising():
    game = game_with()
    quit_now, message = handle_key(game, "u")

    assert not quit_now
    assert "nothing to undo" in message


def test_keys_are_case_insensitive():
    game = game_with(hand="B5 B5", discards="B5")
    handle_key(game, "P")

    assert len(game.melds) == 1
