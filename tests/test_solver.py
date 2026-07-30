import pytest

from mahjong.solver import (
    CHOW,
    PUNG,
    completions,
    decompose,
    is_winning_hand,
    winning_tiles,
)
from mahjong.tiles import Tile, parse_hand


def hand(text):
    return parse_hand(text)


# --------------------------------------------------------------------------
# Regressions for two bugs in the pre-2026 solver. Both fail against it.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("rank", range(1, 10))
def test_a_pair_of_any_rank_can_complete_a_hand(rank):
    """The old solver generated candidate pairs over ranks 1-8 only.

    Tiles are dealt 1-9, so a winning hand whose pair was nines was reported
    as a loss. Parametrised across every rank so the boundary cannot rot back.
    """
    tiles = hand("B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6") + [
        Tile(Tile.parse("D1").suit, rank)
    ] * 2

    assert is_winning_hand(tiles), "pair of %ds should complete the hand" % rank


@pytest.mark.parametrize("rank", range(1, 10))
def test_a_pung_of_any_rank_can_complete_a_hand(rank):
    """Same off-by-one, on triplets rather than pairs."""
    dot = Tile.parse("D1").suit
    tiles = (
        hand("B1 B2 B3 B4 B5 B6 C1 C2 C3 C5 C5")
        + [Tile(dot, rank)] * 3
    )

    assert is_winning_hand(tiles), "pung of %ds should complete the hand" % rank


def test_a_hand_with_leftover_tiles_is_not_a_win():
    """The old solver returned as soon as it had four melds and a pair.

    Tiles in a suit it had not reached yet were never looked at, so a
    sixteen-tile hand with two unusable tiles was reported as mahjong.
    """
    winner = hand("DG DG B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6")
    assert is_winning_hand(winner)

    assert not is_winning_hand(winner + hand("D1 D5"))
    assert not is_winning_hand(winner + hand("D1 D5 D9 C9"))


# --------------------------------------------------------------------------
# Winning hands
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text,description",
    [
        ("B1 B2 B3 B4 B5 B6 B7 B8 B9 C1 C2 C3 D5 D5", "chows across two suits"),
        ("B1 B1 B1 C2 C2 C2 D3 D3 D3 B7 B7 B7 D9 D9", "four pungs"),
        ("DG DG DG DR DR DR WE WE WE WW WW WW B5 B5", "all honours"),
        ("B1 B1 B1 B2 B3 B4 C7 C8 C9 D1 D2 D3 WE WE", "mixed, honour pair"),
        ("B9 B9 B9 C9 C9 C9 D9 D9 D9 B7 B8 B9 C1 C1", "nines everywhere"),
        ("B1 B2 B3 B1 B2 B3 B1 B2 B3 B1 B2 B3 B5 B5", "four identical chows"),
    ],
)
def test_known_winning_hands(text, description):
    assert is_winning_hand(hand(text)), description


@pytest.mark.parametrize(
    "text,description",
    [
        ("B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6 D1 D5", "pair is two different tiles"),
        ("B1 B2 B4 B5 B6 B7 C1 C2 C3 C4 C5 C6 D5 D5", "a gap breaks the run"),
        ("DG DG B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C7", "one tile out of place"),
        ("B1 B1 B4 B4 B7 B7 C1 C1 C4 C4 C7 C7 D5 D5", "seven pairs is not a win here"),
        ("DG DG DG DG B1 B2 B3 B4 B5 B6 C1 C2 C3 C4", "four honours cannot meld"),
        ("B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6", "twelve tiles, no pair"),
        ("B9 C1 D5 WE WS WW WN DG DR DW B3 C7 D2 B6", "nothing melds at all"),
    ],
)
def test_known_losing_hands(text, description):
    assert not is_winning_hand(hand(text)), description


def test_honours_cannot_form_a_run():
    """Winds are ordered in the enum but must never chow."""
    assert not is_winning_hand(hand("WE WS WW B1 B2 B3 C1 C2 C3 D1 D2 D3 D5 D5"))


def test_a_run_cannot_cross_suits():
    assert not is_winning_hand(hand("B1 C2 D3 B4 B5 B6 C1 C2 C3 D1 D2 D3 D5 D5"))


def test_a_run_cannot_wrap_around_nine():
    assert not is_winning_hand(hand("B8 B9 B1 B4 B5 B6 C1 C2 C3 D1 D2 D3 D5 D5"))


def test_flowers_are_ignored_rather_than_counted():
    winner = hand("DG DG B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6")

    assert is_winning_hand(winner + hand("FL FL"))


# --------------------------------------------------------------------------
# Decomposition detail
# --------------------------------------------------------------------------


def test_decomposition_names_its_melds():
    result = decompose(hand("B1 B2 B3 C5 C5 C5 D1 D2 D3 WE WE WE B9 B9"))

    assert result.is_winning
    kinds = sorted(meld.kind for meld in result.melds)
    assert kinds == [CHOW, CHOW, PUNG, PUNG]
    assert result.pair[0].code == "B9"


def test_decomposition_accounts_for_every_tile():
    tiles = hand("B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6 D5 D5")
    result = decompose(tiles)

    assert result.tiles == tuple(sorted(tiles))


def test_decomposition_handles_a_partial_hand():
    """3n+2 tiles decompose even when that is fewer than four melds."""
    result = decompose(hand("B1 B2 B3 D5 D5"))

    assert result is not None
    assert not result.is_winning
    assert len(result.melds) == 1


def test_a_pung_is_preferred_when_a_chow_would_strand_tiles():
    """B1 B1 B1 B2 B3 B4 only works if B1 B1 B1 is read as a pung."""
    result = decompose(hand("B1 B1 B1 B2 B3 B4 C1 C2 C3 D1 D2 D3 D5 D5"))

    assert result is not None and result.is_winning


def test_backtracking_finds_a_chow_reading_when_the_pung_fails():
    """B1 B1 B1 B2 B2 B2 B3 B3 B3 reads as three pungs or three chows."""
    assert is_winning_hand(hand("B1 B1 B1 B2 B2 B2 B3 B3 B3 C1 C2 C3 D5 D5"))


@pytest.mark.parametrize("size", [0, 1, 3, 4, 6, 13, 15, 16])
def test_impossible_hand_sizes_do_not_decompose(size):
    tiles = [Tile.parse("B1")] * size
    if (size - 2) % 3 == 0 and size >= 2:
        pytest.skip("size %d is a legal shape" % size)
    assert decompose(tiles) is None


def test_decompose_of_an_empty_hand_is_none():
    assert decompose([]) is None


# --------------------------------------------------------------------------
# What completes a hand
# --------------------------------------------------------------------------


def test_winning_tiles_finds_a_single_wait():
    tiles = hand("B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6 D5")

    assert [t.code for t in winning_tiles(tiles)] == ["D5"]


def test_winning_tiles_finds_a_two_sided_wait():
    """B1 B2 waiting to become a run can be completed at either end."""
    tiles = hand("B1 B2 B4 B5 B6 C1 C2 C3 C4 C5 C6 D5 D5")

    assert sorted(t.code for t in winning_tiles(tiles)) == ["B3"]


def test_winning_tiles_respects_what_is_left():
    tiles = hand("B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6 D5")
    exhausted = {Tile.parse("D5"): 0}

    assert winning_tiles(tiles, available=exhausted) == []


def test_winning_tiles_of_a_dead_hand_is_empty():
    tiles = hand("B1 B4 B7 C1 C4 C7 D1 D4 D7 WE WS WW WN")

    assert winning_tiles(tiles) == []


def test_completions_for_two_missing_tiles():
    tiles = hand("B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6")
    found = completions(tiles)

    assert all(len(combo) == 2 for combo in found)
    assert all(is_winning_hand(tiles + list(combo)) for combo in found)

    pairs = [c for c in found if c[0] == c[1]]
    assert len(pairs) == 34, "any of the 34 tile types can serve as the pair"


def test_completions_need_not_be_the_pair_themselves():
    """Drawn tiles can rearrange existing runs instead of pairing up.

    Adding B1 and B4 to B1-B6 gives B1 B1 as the pair with B2 B3 B4 and
    B4 B5 B6 as the runs -- neither drawn tile is the pair.
    """
    tiles = hand("B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6")
    found = completions(tiles)

    reshuffles = [c for c in found if c[0] != c[1]]
    assert (Tile.parse("B1"), Tile.parse("B4")) in reshuffles
    assert len(reshuffles) == 8


def test_completions_of_an_already_complete_hand_is_the_empty_draw():
    tiles = hand("B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6 D5 D5")

    assert completions(tiles) == [()]


def test_completions_of_an_overfull_hand_is_empty():
    tiles = hand("B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6 D5 D5 D9")

    assert completions(tiles) == []


def test_completions_are_limited_by_availability():
    tiles = hand("B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6")
    only_dots = {Tile.parse("D5"): 2}

    found = completions(tiles, available=only_dots)

    assert found == [(Tile.parse("D5"), Tile.parse("D5"))]


def test_completions_will_not_ask_for_more_copies_than_exist():
    tiles = hand("B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6")
    one_left = {Tile.parse("D5"): 1}

    assert completions(tiles, available=one_left) == []
