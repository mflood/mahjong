from suit import Suit
from tile import Tile
import curses

def print_tiles(window, tiles, last_tile):

    if not last_tile:
        last_tile = Tile(Suit.NONE)

    counts = {}
    
    words = {
        Suit.BAM: " BAM",
        Suit.CRAK: "CRAK",
        Suit.DOT: " DOT",
        Suit.GREEN_DRAGON: "G",
        Suit.WHITE_DRAGON: "W",
        Suit.RED_DRAGON: "R",
        Suit.EAST_WIND: "E",
        Suit.WEST_WIND: "W",
        Suit.NORTH_WIND: "N",
        Suit.SOUTH_WIND: "S",
        Suit.FLOWER: "*",
    }
    
    for word in [Suit.BAM, Suit.CRAK, Suit.DOT]: 
        counts.setdefault(word, {})
        for x in range(1, 10):
            counts[word].setdefault(x, 0)

    for suit in [Suit.GREEN_DRAGON,
                 Suit.WHITE_DRAGON,
                 Suit.RED_DRAGON,
                 Suit.EAST_WIND,
                 Suit.WEST_WIND,
                 Suit.NORTH_WIND,
                 Suit.SOUTH_WIND,
                 Suit.FLOWER,
                 ]:
        counts.setdefault(suit, 0)


    for tile in tiles:
        if tile.suit in [Suit.BAM, Suit.CRAK, Suit.DOT]:
            counts[tile.suit][tile.number] += 1
        else:
            counts[tile.suit] += 1

    # Print row titles
    for offset, word in enumerate([Suit.BAM, Suit.CRAK, Suit.DOT]):
        for idx, t in enumerate(range(4)):
            window.addstr(offset * 5 + idx, 0, words[word], curses.color_pair(1))
    
    # Print regulars
    for z, suit in enumerate([Suit.BAM, Suit.CRAK, Suit.DOT]):
        for x in range(1, 10):
            amount = counts[suit][x]
            for y in range(4):
                color = 0
                if y < amount:
                    char = str(x)
                    if suit == last_tile.suit and x == last_tile.number:
                        color = curses.color_pair(1)
                else:
                    char = "."
                window.addstr(z * 5 + y, 6 + x * 2, char, color)
    
    # Print the Dragons
    for z, suit in enumerate([Suit.GREEN_DRAGON, Suit.WHITE_DRAGON, Suit.RED_DRAGON]):
        amount = counts[suit]
        for y in range(4):
            color = 0
            if y < amount:
                char = words[suit]
                if suit == last_tile.suit:
                    color = curses.color_pair(1)
            else:
                char = "."

            window.addstr(z * 5 + y, 6 + 9 * 2 + 3, char, color)

    # Print the NORTH/EAST WIND
    for z, suit in enumerate([Suit.NORTH_WIND, Suit.EAST_WIND]):
        amount = counts[suit]
        for y in range(4):
            color = 0
            if y < amount:
                char = words[suit]
                if suit == last_tile.suit:
                    color = curses.color_pair(1)
            else:
                char = "."

            window.addstr(z * 5 + y, 6 + 9 * 2 + 3 + 4, char, color)

    # Print the SOUTH/WEST WIND
    for z, suit in enumerate([Suit.SOUTH_WIND, Suit.WEST_WIND]):
        amount = counts[suit]
        for y in range(4):
            color = 0
            if y < amount:
                char = words[suit]
                if suit == last_tile.suit:
                    color = curses.color_pair(1)
            else:
                char = "."

            window.addstr(z * 5 + y, 6 + 9 * 2 + 3 + 4 + 2, char, color)

    # Print the Flowers
    amount = counts[Suit.FLOWER]
    for y in range(8):
        if y < amount:
            char = '*'
        else:
            char = "."

        window.addstr(2 * 5 + 5, y * 2 + 8, char)

    window.refresh()

