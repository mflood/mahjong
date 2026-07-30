from mahjong.actions import ClaimPung, DrawFromWall
from mahjong.game import OPENING_HAND_SIZE, Game
from mahjong.hand import Discards, Hand
from mahjong.tiles import Tile, parse_hand
from mahjong.wall import TILES_IN_A_SET, Wall


def game_with(hand="", wall="", discards=""):
    return Game(
        wall=Wall(tiles=parse_hand(wall)),
        hand=Hand(parse_hand(hand)),
        discards=Discards(parse_hand(discards)),
    )


def test_a_new_game_has_a_full_shuffled_wall():
    game = Game(seed=1)

    assert len(game.wall) == TILES_IN_A_SET
    assert len(game.hand) == 0


def test_dealing_fills_the_opening_hand():
    game = Game(seed=1)
    game.deal()

    assert len(game.hand) + len(game.hand.flowers) >= OPENING_HAND_SIZE
    assert len(game.hand) == OPENING_HAND_SIZE


def test_a_seeded_game_deals_the_same_hand_twice():
    first, second = Game(seed=9), Game(seed=9)
    first.deal()
    second.deal()

    assert str(first.hand) == str(second.hand)


def test_all_tiles_includes_claimed_melds():
    """A claimed meld leaves the concealed hand but stays part of the hand."""
    game = game_with(hand="B5 B5 C1", discards="B5")
    game.perform(ClaimPung(game))

    assert len(game.hand) == 1
    assert len(game.all_tiles) == 4


def test_a_hand_can_win_after_claiming_a_meld():
    """The whole point of all_tiles: melded tiles must count towards the win."""
    game = game_with(hand="B1 B2 B3 B4 B5 B6 C1 C2 C3 D5 D5 DG DG", discards="DG")

    assert not game.is_winning()
    game.perform(ClaimPung(game))

    assert len(game.hand) == 11
    assert game.is_winning(), "10 concealed + a claimed pung is still fourteen tiles"


def test_waiting_on_accounts_for_melds():
    game = game_with(
        hand="B1 B2 B3 B4 B5 B6 C1 C2 C3 D5 DG DG", discards="DG", wall="D5"
    )
    game.perform(ClaimPung(game))

    assert [t.code for t in game.waiting_on()] == ["D5"]


def test_waiting_on_is_limited_to_tiles_still_in_the_wall():
    game = game_with(hand="B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6 D5", wall="B9")

    assert game.waiting_on() == []


def test_hand_is_full_counts_melds():
    game = game_with(hand="B5 B5 C1", discards="B5")

    assert not game.hand_is_full
    game.hand._tiles.extend(parse_hand("B1 B2 B3 B4 B5 B6 C2 C3 C4 C5 C6"))

    assert game.hand_is_full


def test_snapshot_and_restore_round_trip_everything():
    game = game_with(hand="B1", wall="C9 D9", discards="B7")
    snapshot = game.snapshot()

    game.perform(DrawFromWall(game))
    game.melds.append(tuple(parse_hand("C1 C2 C3")))
    game.restore(snapshot)

    assert str(game.hand) == "B1"
    assert len(game.wall) == 2
    assert str(game.discards) == "B7"
    assert game.melds == []


def test_history_records_performed_actions():
    game = game_with(wall="B1 B2")
    game.perform(DrawFromWall(game))
    game.perform(DrawFromWall(game))

    assert len(game.history) == 2
    assert game.can_undo

    game.undo()
    assert len(game.history) == 1
