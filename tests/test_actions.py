import pytest

from mahjong.actions import (
    ClaimChow,
    ClaimPung,
    DiscardFromWall,
    DiscardLastDrawn,
    DiscardTile,
    DrawFromWall,
    TakeFromWall,
)
from mahjong.errors import ActionNotAllowed
from mahjong.game import Game
from mahjong.hand import Discards, Hand
from mahjong.tiles import Tile, parse_hand
from mahjong.wall import Wall


def game_with(hand="", wall="", discards=""):
    return Game(
        wall=Wall(tiles=parse_hand(wall)),
        hand=Hand(parse_hand(hand)),
        discards=Discards(parse_hand(discards)),
    )


def test_draw_moves_a_tile_from_wall_to_hand():
    game = game_with(wall="B1")
    game.perform(DrawFromWall(game))

    assert str(game.hand) == "B1"
    assert len(game.wall) == 0


def test_draw_from_an_empty_wall_is_not_allowed():
    game = game_with()

    assert not DrawFromWall(game).is_allowed()
    with pytest.raises(ActionNotAllowed):
        DrawFromWall(game).execute()


def test_take_pulls_a_named_tile_out_of_the_wall():
    game = game_with(wall="B1 C5 D9")
    game.perform(TakeFromWall(game, Tile.parse("C5")))

    assert str(game.hand) == "C5"
    assert Tile.parse("C5") not in game.wall.tiles


def test_take_of_an_absent_tile_is_not_allowed():
    game = game_with(wall="B1")

    assert not TakeFromWall(game, Tile.parse("C5")).is_allowed()


def test_discard_moves_a_chosen_tile_to_the_pile():
    game = game_with(hand="B1 C5")
    game.perform(DiscardTile(game, Tile.parse("B1")))

    assert str(game.hand) == "C5"
    assert str(game.discards) == "B1"


def test_discarding_a_tile_you_do_not_hold_is_not_allowed():
    game = game_with(hand="B1")

    assert not DiscardTile(game, Tile.parse("C5")).is_allowed()


def test_discard_last_throws_away_what_was_just_drawn():
    game = game_with(hand="B1 B2", wall="C9")
    game.perform(DrawFromWall(game))
    game.perform(DiscardLastDrawn(game))

    assert str(game.hand) == "B1 B2"
    assert str(game.discards) == "C9"


def test_discard_last_on_an_empty_hand_is_not_allowed():
    game = game_with()

    assert not DiscardLastDrawn(game).is_allowed()


def test_burn_sends_a_wall_tile_straight_to_the_discards():
    game = game_with(wall="B7")
    game.perform(DiscardFromWall(game))

    assert len(game.hand) == 0
    assert str(game.discards) == "B7"


# --------------------------------------------------------------------------
# Claiming melds
# --------------------------------------------------------------------------


def test_pung_claims_a_discard_with_two_from_hand():
    game = game_with(hand="B5 B5 C1", discards="B5")
    game.perform(ClaimPung(game))

    assert game.melds == [tuple(parse_hand("B5 B5 B5"))]
    assert str(game.hand) == "C1"
    assert len(game.discards) == 0


def test_pung_needs_two_matching_tiles_in_hand():
    game = game_with(hand="B5 C1", discards="B5")

    assert not ClaimPung(game).is_allowed()


def test_chow_claims_the_bottom_of_a_run():
    game = game_with(hand="B2 B3 C1", discards="B1")
    game.perform(ClaimChow(game))

    assert game.melds == [tuple(parse_hand("B1 B2 B3"))]
    assert str(game.hand) == "C1"


def test_chow_claims_the_middle_of_a_run():
    game = game_with(hand="B1 B3", discards="B2")
    game.perform(ClaimChow(game))

    assert game.melds == [tuple(parse_hand("B1 B2 B3"))]


def test_chow_claims_the_top_of_a_run():
    game = game_with(hand="B1 B2", discards="B3")
    game.perform(ClaimChow(game))

    assert game.melds == [tuple(parse_hand("B1 B2 B3"))]


def test_chow_does_not_run_off_the_bottom_of_a_suit():
    """Claiming B1 must not try to build a run starting at B-minus-one."""
    game = game_with(hand="B2 B3 B4", discards="B1")
    action = ClaimChow(game)

    assert action.is_allowed()
    action.execute()
    assert game.melds == [tuple(parse_hand("B1 B2 B3"))]


def test_chow_does_not_run_off_the_top_of_a_suit():
    game = game_with(hand="B7 B8", discards="B9")
    game.perform(ClaimChow(game))

    assert game.melds == [tuple(parse_hand("B7 B8 B9"))]


def test_chow_cannot_cross_suits():
    game = game_with(hand="C2 D3", discards="B1")

    assert not ClaimChow(game).is_allowed()


def test_chow_cannot_use_honours():
    game = game_with(hand="WS WW", discards="WE")

    assert not ClaimChow(game).is_allowed()


def test_claiming_with_an_empty_discard_pile_is_not_allowed():
    game = game_with(hand="B1 B2")

    assert not ClaimChow(game).is_allowed()
    assert not ClaimPung(game).is_allowed()


# --------------------------------------------------------------------------
# Undo
# --------------------------------------------------------------------------


def test_undo_restores_the_previous_state():
    game = game_with(hand="B1", wall="C9")
    before = str(game.hand), len(game.wall)

    game.perform(DrawFromWall(game))
    game.undo()

    assert (str(game.hand), len(game.wall)) == before


def test_undo_unwinds_several_actions_in_order():
    game = game_with(hand="B1 B2 B3", wall="C9 D9")
    start = str(game.hand)

    game.perform(DrawFromWall(game))
    game.perform(DrawFromWall(game))
    game.perform(DiscardTile(game, Tile.parse("B1")))

    while game.can_undo:
        game.undo()

    assert str(game.hand) == start
    assert len(game.wall) == 2
    assert len(game.discards) == 0


def test_undo_puts_a_claimed_meld_back():
    game = game_with(hand="B5 B5 C1", discards="B5")
    game.perform(ClaimPung(game))
    game.undo()

    assert game.melds == []
    assert str(game.hand) == "B5 B5 C1"
    assert str(game.discards) == "B5"


def test_undo_with_nothing_to_undo_raises():
    game = game_with()

    with pytest.raises(ActionNotAllowed, match="nothing to undo"):
        game.undo()


def test_an_action_cannot_be_undone_twice():
    game = game_with(hand="B1", wall="C9")
    action = game.perform(DrawFromWall(game))
    action.undo()

    with pytest.raises(ActionNotAllowed, match="has not been performed"):
        action.undo()
