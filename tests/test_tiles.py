import pytest

from mahjong.errors import InvalidTile
from mahjong.tiles import (
    HONOUR_SUITS,
    NUMBERED_SUITS,
    Suit,
    Tile,
    all_tile_types,
    format_hand,
    parse_hand,
)


@pytest.mark.parametrize(
    "code,suit,rank",
    [
        ("B1", Suit.BAMBOO, 1),
        ("C5", Suit.CHARACTER, 5),
        ("D9", Suit.DOT, 9),
        ("WE", Suit.EAST_WIND, None),
        ("WN", Suit.NORTH_WIND, None),
        ("DG", Suit.GREEN_DRAGON, None),
        ("DW", Suit.WHITE_DRAGON, None),
        ("FL", Suit.FLOWER, None),
    ],
)
def test_parse_round_trips(code, suit, rank):
    tile = Tile.parse(code)

    assert (tile.suit, tile.rank) == (suit, rank)
    assert tile.code == code


def test_d_prefix_is_unambiguous():
    """D9 is nine dots; DW is the white dragon. The second character decides."""
    assert Tile.parse("D9").suit is Suit.DOT
    assert Tile.parse("DW").suit is Suit.WHITE_DRAGON


def test_parsing_is_case_insensitive():
    assert Tile.parse("b3") == Tile.parse("B3")
    assert Tile.parse("dg") == Tile.parse("DG")


@pytest.mark.parametrize("bad", ["", "B", "B0", "Z1", "B10", "XX", "B99", "1B"])
def test_parse_rejects_junk(bad):
    with pytest.raises(InvalidTile):
        Tile.parse(bad)


def test_numbered_tiles_require_a_rank_in_range():
    with pytest.raises(InvalidTile, match="need a rank"):
        Tile(Suit.BAMBOO)
    with pytest.raises(InvalidTile, match="outside"):
        Tile(Suit.BAMBOO, 0)
    with pytest.raises(InvalidTile, match="outside"):
        Tile(Suit.BAMBOO, 10)


def test_honours_reject_a_rank():
    with pytest.raises(InvalidTile, match="no rank"):
        Tile(Suit.EAST_WIND, 3)


def test_suit_classification():
    assert Tile.parse("B5").is_numbered
    assert not Tile.parse("B5").is_honour
    assert Tile.parse("WE").is_honour
    assert Tile.parse("FL").is_bonus
    assert not Tile.parse("DG").is_bonus


def test_successor_walks_up_a_suit_and_stops_at_nine():
    assert Tile.parse("B1").successor() == Tile.parse("B2")
    assert Tile.parse("B9").successor() is None
    assert Tile.parse("WE").successor() is None


def test_tiles_are_hashable_and_compare_by_value():
    assert Tile.parse("B3") == Tile.parse("B3")
    assert len({Tile.parse("B3"), Tile.parse("B3")}) == 1
    assert Tile.parse("B3") != Tile.parse("C3")


def test_tiles_sort_by_suit_then_rank():
    tiles = parse_hand("D1 B9 B1 C5 WE")

    assert format_hand(tiles) == "B1 B9 C5 D1 WE"


def test_names_read_naturally():
    assert Tile.parse("B5").name == "5 Bamboo"
    assert Tile.parse("DG").name == "Green Dragon"


def test_parse_hand_accepts_commas_and_extra_space():
    assert format_hand(parse_hand("B1,  B2 ,B3")) == "B1 B2 B3"


def test_parse_hand_of_nothing_is_empty():
    assert parse_hand("   ") == []


def test_all_tile_types_covers_the_game_minus_flowers():
    types = all_tile_types()

    assert len(types) == len(NUMBERED_SUITS) * 9 + len(HONOUR_SUITS)
    assert len(types) == 34
    assert not any(t.is_bonus for t in types)
    assert len(set(types)) == len(types)
