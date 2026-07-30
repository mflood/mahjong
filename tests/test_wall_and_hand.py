from collections import Counter

import pytest

from mahjong.errors import TileNotPresent, WallEmpty
from mahjong.hand import Discards, Hand
from mahjong.tiles import Suit, Tile, parse_hand
from mahjong.wall import COPIES_OF_EACH_TILE, TILES_IN_A_SET, Wall, full_set

# --------------------------------------------------------------------------
# Wall
# --------------------------------------------------------------------------


def test_a_full_set_is_one_hundred_and_forty_four_tiles():
    tiles = full_set()

    assert len(tiles) == TILES_IN_A_SET == 144


def test_every_playing_tile_appears_four_times():
    counts = Counter(t for t in full_set() if not t.is_bonus)

    assert set(counts.values()) == {COPIES_OF_EACH_TILE}
    assert len(counts) == 34


def test_there_are_eight_flowers():
    flowers = [t for t in full_set() if t.is_bonus]

    assert len(flowers) == 8


def test_shuffle_is_reproducible_with_a_seed():
    first = Wall(seed=7).shuffle()
    second = Wall(seed=7).shuffle()

    assert first.tiles == second.tiles


def test_different_seeds_give_different_orders():
    assert Wall(seed=1).shuffle().tiles != Wall(seed=2).shuffle().tiles


def test_shuffle_keeps_every_tile():
    wall = Wall(seed=3)
    before = Counter(wall.tiles)
    wall.shuffle()

    assert Counter(wall.tiles) == before


def test_drawing_shrinks_the_wall():
    wall = Wall()
    size = len(wall)
    wall.draw()

    assert len(wall) == size - 1


def test_dealing_takes_several_at_once():
    wall = Wall()
    dealt = wall.deal(13)

    assert len(dealt) == 13
    assert len(wall) == TILES_IN_A_SET - 13


def test_drawing_from_an_empty_wall_raises():
    wall = Wall(tiles=[])

    with pytest.raises(WallEmpty):
        wall.draw()


def test_take_removes_a_named_tile():
    wall = Wall()
    tile = Tile(Suit.BAMBOO, 5)

    assert wall.take(tile) == tile
    assert Counter(wall.tiles)[tile] == COPIES_OF_EACH_TILE - 1


def test_take_of_an_absent_tile_raises():
    wall = Wall(tiles=parse_hand("B1 B2"))

    with pytest.raises(TileNotPresent, match="C9"):
        wall.take(Tile.parse("C9"))


def test_counts_reports_what_remains():
    wall = Wall(tiles=parse_hand("B1 B1 C5"))

    assert wall.counts() == {Tile.parse("B1"): 2, Tile.parse("C5"): 1}


# --------------------------------------------------------------------------
# Hand
# --------------------------------------------------------------------------


def test_a_hand_keeps_its_tiles_sorted():
    hand = Hand(parse_hand("D1 B9 B1"))

    assert str(hand) == "B1 B9 D1"


def test_adding_records_the_last_tile():
    hand = Hand(parse_hand("B1"))
    hand.add(Tile.parse("C5"))

    assert hand.last_tile == Tile.parse("C5")


def test_flowers_are_held_apart_from_the_concealed_tiles():
    hand = Hand(parse_hand("B1 FL B2 FL"))

    assert str(hand) == "B1 B2"
    assert len(hand.flowers) == 2
    assert len(hand) == 2


def test_adding_a_flower_does_not_join_the_hand():
    hand = Hand(parse_hand("B1"))
    hand.add(Tile.parse("FL"))

    assert len(hand) == 1
    assert len(hand.flowers) == 1


def test_removing_a_tile_that_is_not_held_raises():
    hand = Hand(parse_hand("B1 B2"))

    with pytest.raises(TileNotPresent, match="C9"):
        hand.remove(Tile.parse("C9"))


def test_removing_one_of_a_duplicate_keeps_the_other():
    hand = Hand(parse_hand("B1 B1 C5"))
    hand.remove(Tile.parse("B1"))

    assert str(hand) == "B1 C5"


def test_last_tile_survives_removing_a_duplicate_of_it():
    """Discarding one B1 while holding two must not blank the last tile."""
    hand = Hand(parse_hand("B1 C5"))
    hand.add(Tile.parse("B1"))
    hand.remove(Tile.parse("B1"))

    assert hand.last_tile == Tile.parse("B1")


def test_last_tile_clears_when_the_final_copy_goes():
    hand = Hand(parse_hand("C5"))
    hand.add(Tile.parse("B1"))
    hand.remove(Tile.parse("B1"))

    assert hand.last_tile == Tile.parse("C5")


def test_state_round_trips_for_undo():
    hand = Hand(parse_hand("B1 B2 FL"))
    snapshot = hand.state()

    hand.add(Tile.parse("C9"))
    hand.remove(Tile.parse("B1"))
    hand.restore(snapshot)

    assert str(hand) == "B1 B2"
    assert len(hand.flowers) == 1


def test_a_hand_knows_when_it_has_won():
    hand = Hand(parse_hand("B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6 D5 D5"))

    assert hand.is_winning()
    assert hand.decomposition().is_winning


def test_a_hand_reports_what_it_waits_on():
    hand = Hand(parse_hand("B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6 D5"))

    assert [t.code for t in hand.waiting_on()] == ["D5"]


def test_discards_behave_like_any_other_pile():
    discards = Discards()
    discards.add(Tile.parse("B1"))

    assert Tile.parse("B1") in discards
    assert len(discards) == 1
