"""Deciding whether a hand is complete, and what would complete it.

A winning hand under Chinese/Hong Kong rules is four melds plus one pair —
fourteen tiles. A meld is a *pung* (three identical tiles) or a *chow* (three
consecutive tiles in one suit). Honours pair and pung but never chow, and
flowers are set aside rather than counted.

The decomposition works on tile *counts* rather than tile lists. Pick the pair
first — there are at most a handful of candidates — then partition what remains
suit by suit. Within a numbered suit the partition is deterministic backtracking
on the lowest remaining rank: it is either the bottom of a chow or part of a
pung, so there are only two branches to try and the recursion depth is bounded
by the tiles in that suit.
"""

from collections import Counter
from dataclasses import dataclass
from itertools import combinations_with_replacement

from .tiles import MAX_RANK, MIN_RANK, NUMBERED_SUITS, Tile, all_tile_types

TILES_IN_A_PAIR = 2
TILES_IN_A_MELD = 3
MELDS_IN_A_WINNING_HAND = 4
WINNING_HAND_SIZE = MELDS_IN_A_WINNING_HAND * TILES_IN_A_MELD + TILES_IN_A_PAIR

PUNG = "pung"
CHOW = "chow"


@dataclass(frozen=True)
class Meld:
    """Three tiles forming a set."""

    tiles: tuple

    @property
    def kind(self):
        return PUNG if self.tiles[0] == self.tiles[-1] else CHOW

    def __str__(self):
        return " ".join(t.code for t in self.tiles)


@dataclass(frozen=True)
class Decomposition:
    """One way of reading a hand as melds plus a pair."""

    melds: tuple
    pair: tuple

    @property
    def is_winning(self):
        return len(self.melds) == MELDS_IN_A_WINNING_HAND

    @property
    def tiles(self):
        flat = [t for meld in self.melds for t in meld.tiles]
        flat.extend(self.pair)
        return tuple(sorted(flat))

    def __str__(self):
        parts = [str(meld) for meld in self.melds]
        parts.append("%s %s" % (self.pair[0].code, self.pair[1].code))
        return " | ".join(parts)


def decompose(tiles):
    """Read `tiles` as melds plus one pair, or return None if it cannot be.

    Flowers are ignored. Works for any hand of size ``3n + 2``, so it is also
    useful mid-game on a partial hand.
    """
    concealed = [t for t in tiles if not t.is_bonus]
    if len(concealed) < TILES_IN_A_PAIR:
        return None
    if (len(concealed) - TILES_IN_A_PAIR) % TILES_IN_A_MELD != 0:
        return None

    expected_melds = (len(concealed) - TILES_IN_A_PAIR) // TILES_IN_A_MELD
    counts = Counter(concealed)

    for candidate in sorted(counts):
        if counts[candidate] < TILES_IN_A_PAIR:
            continue
        remaining = Counter(counts)
        remaining[candidate] -= TILES_IN_A_PAIR
        if remaining[candidate] == 0:
            del remaining[candidate]

        melds = _partition_into_melds(remaining)
        if melds is not None and len(melds) == expected_melds:
            return Decomposition(tuple(melds), (candidate, candidate))

    return None


def is_winning_hand(tiles):
    """True when `tiles` is a complete hand: four melds and a pair.

    Hand size is enforced by construction — four melds plus a pair is fourteen
    tiles, so a hand carrying anything left over cannot satisfy it.
    """
    result = decompose(tiles)
    return result is not None and result.is_winning


def winning_tiles(tiles, available=None):
    """Which single tiles would turn `tiles` into a winning hand.

    `available` optionally maps tiles to how many remain unseen; tiles with
    none left are excluded. Costs one decomposition per distinct tile type —
    thirty-four — rather than enumerating draws from the wall.
    """
    concealed = [t for t in tiles if not t.is_bonus]
    found = []
    for candidate in all_tile_types():
        if available is not None and available.get(candidate, 0) <= 0:
            continue
        if is_winning_hand(concealed + [candidate]):
            found.append(candidate)
    return found


def completions(tiles, available=None, draws=None):
    """Every multiset of `draws` tiles that completes the hand.

    Defaults to however many tiles are missing. Each result is a sorted tuple.
    Candidates are distinct tile *types* limited by `available`, so drawing the
    same tile from four different places is one answer rather than four.
    """
    concealed = [t for t in tiles if not t.is_bonus]
    if draws is None:
        draws = WINNING_HAND_SIZE - len(concealed)
    if draws < 0:
        return []
    if draws == 0:
        return [()] if is_winning_hand(concealed) else []
    if draws == 1:
        return [(t,) for t in winning_tiles(concealed, available)]

    candidates = [
        t
        for t in all_tile_types()
        if available is None or available.get(t, 0) > 0
    ]
    found = []
    for combination in combinations_with_replacement(candidates, draws):
        if available is not None:
            counts = Counter(combination)
            if any(counts[t] > available.get(t, 0) for t in counts):
                continue
        if is_winning_hand(concealed + list(combination)):
            found.append(tuple(sorted(combination)))
    return found


def _partition_into_melds(counts):
    """Split a Counter of tiles into melds, or return None.

    Honours can only form pungs, so any honour not appearing exactly three
    times fails immediately. Numbered suits are handed to the backtracker.
    """
    melds = []

    for tile in sorted(t for t in counts if t.is_honour):
        if counts[tile] != TILES_IN_A_MELD:
            return None
        melds.append(Meld((tile,) * TILES_IN_A_MELD))

    for suit in NUMBERED_SUITS:
        ranks = [0] * (MAX_RANK - MIN_RANK + 1)
        total = 0
        for tile, count in counts.items():
            if tile.suit is suit:
                ranks[tile.rank - MIN_RANK] = count
                total += count
        if total == 0:
            continue
        if total % TILES_IN_A_MELD != 0:
            return None
        found = _partition_suit(suit, ranks)
        if found is None:
            return None
        melds.extend(found)

    return melds


def _partition_suit(suit, ranks):
    """Backtrack over one numbered suit's rank counts. Mutates and restores."""
    index = next((i for i, count in enumerate(ranks) if count), None)
    if index is None:
        return []

    rank = index + MIN_RANK

    if ranks[index] >= TILES_IN_A_MELD:
        ranks[index] -= TILES_IN_A_MELD
        rest = _partition_suit(suit, ranks)
        ranks[index] += TILES_IN_A_MELD
        if rest is not None:
            return [Meld((Tile(suit, rank),) * TILES_IN_A_MELD)] + rest

    if index + 2 < len(ranks) and ranks[index + 1] and ranks[index + 2]:
        ranks[index] -= 1
        ranks[index + 1] -= 1
        ranks[index + 2] -= 1
        rest = _partition_suit(suit, ranks)
        ranks[index] += 1
        ranks[index + 1] += 1
        ranks[index + 2] += 1
        if rest is not None:
            chow = Meld(
                (Tile(suit, rank), Tile(suit, rank + 1), Tile(suit, rank + 2))
            )
            return [chow] + rest

    return None
