# mahjong

[![tests](https://github.com/mflood/mahjong/actions/workflows/tests.yml/badge.svg)](https://github.com/mflood/mahjong/actions/workflows/tests.yml)

A mahjong hand solver, and a terminal table to explore hands with.

Answers the two questions you actually have while holding tiles: **is this a
winning hand**, and **what would complete it**. Chinese/Hong Kong rules — four
melds plus a pair.

No dependencies. Python 3.11 or newer.

## Solving a hand

```
$ mahjong solve B1 B2 B3 C5 C5 C5 D1 D2 D3 WE WE WE B9 B9
hand:  B1 B2 B3 B9 B9 C5 C5 C5 D1 D2 D3 WE WE WE  (14 tiles)
result: winning hand
  pung WE WE WE
  chow B1 B2 B3
  pung C5 C5 C5
  chow D1 D2 D3
  pair B9 B9
```

It exits 0 for a win and 1 otherwise, so it drops into a shell pipeline.
`--json` gives you the melds as data.

## What am I waiting on

```
$ mahjong waiting B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6 D5
hand: B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6 D5  (13 tiles, 1 missing)
completed by:
  D5
```

```
$ mahjong waiting B1 B2 B4 B5 B6 B7 C1 C2 C3 D5 D5 D6 D7
hand: B1 B2 B4 B5 B6 B7 C1 C2 C3 D5 D5 D6 D7  (13 tiles, 1 missing)
nothing completes this hand
```

Give it fewer than thirteen tiles and it reports every combination that would
finish the hand, not just single tiles.

## Tile notation

| | |
|---|---|
| `B1`–`B9` | Bamboo |
| `C1`–`C9` | Characters |
| `D1`–`D9` | Dots |
| `WE` `WS` `WW` `WN` | Winds |
| `DG` `DR` `DW` | Dragons |
| `FL` | Flower |

Nothing is ambiguous: the character after the suit letter is a digit for
numbered tiles and a letter for honours, so `D9` is nine dots and `DW` is the
white dragon. Case-insensitive.

## The table

`mahjong play` deals a hand and opens a curses table that keeps the analysis
live as you draw and discard:

```
HAND
  B1 B2 B3 B4 B5 B6 C1 C2 C3 D5
  melds: DG DG DG

ANALYSIS
  13 of 14 tiles
  waiting on: D5

DISCARDS
  B8 C9 D2 WE

wall 144   discards 4   undo available
space  draw a tile from the wall
b      burn a wall tile to the discards
d      discard the tile you just drew
p      claim the last discard as a pung
c      claim the last discard as a chow
u      undo
q      quit
```

Every action is undoable, including claims. Actions snapshot the game before
touching it and undo by restoring, rather than each one hand-writing its own
inverse — which is the difference between undo you can trust and undo that
drifts out of step the first time an action grows a second effect.

## As a library

```python
from mahjong import parse_hand, is_winning_hand, winning_tiles, decompose

tiles = parse_hand("B1 B2 B3 C5 C5 C5 D1 D2 D3 WE WE WE B9 B9")
is_winning_hand(tiles)          # True
str(decompose(tiles))           # 'WE WE WE | B1 B2 B3 | C5 C5 C5 | D1 D2 D3 | B9 B9'

waiting = parse_hand("B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6 D5")
[t.code for t in winning_tiles(waiting)]   # ['D5']
```

## How the solver works

A winning hand is four melds and a pair. A meld is a *pung* (three identical
tiles) or a *chow* (three consecutive tiles in one suit). Honours pair and pung
but never chow; flowers are set aside.

The decomposition works on tile **counts**, not tile lists:

1. **Pick the pair.** Only tiles held at least twice are candidates, so there
   are a handful at most. Try each.
2. **Partition what's left, suit by suit.** Honours must appear exactly three
   times or the hand fails immediately. Numbered suits go to a backtracker.
3. **Within a suit, work from the lowest remaining rank.** That tile is either
   part of a pung or the bottom of a chow — only two branches, and each
   consumes three tiles, so recursion depth is bounded by the suit's size.

`winning_tiles` then costs one decomposition per distinct tile type — thirty-four
— rather than enumerating draws from a wall of a hundred-odd tiles. That is what
makes the table's live analysis cheap enough to run on every keystroke.

| Module | Responsibility |
|---|---|
| `mahjong/tiles.py` | Suits, tiles, notation |
| `mahjong/solver.py` | Decomposition, `is_winning_hand`, `winning_tiles` |
| `mahjong/wall.py` | The 144-tile set, shuffling, drawing |
| `mahjong/hand.py` | Hands and discard piles |
| `mahjong/actions.py` | Draw, discard, claim — each undoable |
| `mahjong/game.py` | State and undo history |
| `mahjong/ui/render.py` | Game state → lines of text (no curses) |
| `mahjong/ui/keys.py` | Keystroke → action (no curses) |
| `mahjong/ui/table.py` | The only module that imports curses |

## Tests

```bash
pip install -r requirements-dev.txt
PYTHONPATH=. python -m pytest tests -v
```

180 tests, no terminal required. The interface is split so that everything it
*decides* — what to show, which key does what, what happens when an action is
refused — is a plain function returning strings, and `table.py` only paints
them. CI runs on Python 3.11 and 3.12.

## History

Written over two weeks in February 2020 and left where it stopped. The 2026
rebuild kept the ideas — the action objects, the live "what completes this
hand" analysis — and fixed two bugs in the solver that had been there the whole
time:

- **Pairs and pungs of nines were invisible.** Candidate sets were generated
  over `range(1, 9)` — ranks 1 to 8 — while the wall deals 1 to 9. A genuine
  winning hand whose pair was nines scored as a loss. The tests now parametrise
  every rank, so that boundary cannot rot back.
- **Hands with leftover tiles were declared winners.** The check returned as
  soon as it had four melds and a pair, so tiles in a suit it had not yet
  reached were never examined, and a sixteen-tile hand with two unusable tiles
  came back as mahjong. Hand size is now enforced by construction — four melds
  plus a pair is fourteen tiles, and anything left over cannot satisfy that.

Also fixed on the way through: `fast_tile_chooser.py` contained
`if suit = suit_map.get(k):` and had not parsed in years, and `mahjong.py` was
an abandoned earlier prototype referencing undefined names.

## License

Apache 2.0 — see [LICENSE](LICENSE).
