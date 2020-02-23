from curses import wrapper
import curses
import time
from wall import Wall
from hand import Hand
import random
from tile import Tile

from suit import Suit
from discards import Discards

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

def main(stdscr):
    # Clear screen
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    wall = Wall()
    hand = Hand()
    discards = Discards()
    wall.load_tiles()
    wall.shuffle()

    #for x in range(15 * 4):
    #    t = wall.draw()
    #    discards.add(t)

    #for x in range(13):
    #    t = wall.draw()
    #    hand.add(t)

    height = 30
    width = 40
    begin_y = 5
    begin_x = 5

    wall_window = curses.newwin(height, width, begin_y, begin_x)
    discard_window = curses.newwin(height, width, begin_y, begin_x + 45)
    hand_window = curses.newwin(height, width, begin_y + 20, begin_x)
    command_window = curses.newwin(3, 100, 2, 2)

    print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
    print_tiles(discard_window, discards.tiles, discards.last_tile)
    print_tiles(hand_window, hand.tiles, hand.last_tile)

    dragons = [Suit.GREEN_DRAGON, Suit.WHITE_DRAGON, Suit.RED_DRAGON]
    num_suits = [Suit.BAM, Suit.CRAK, Suit.DOT]
    winds = [Suit.NORTH_WIND, Suit.SOUTH_WIND, Suit.EAST_WIND, Suit.WEST_WIND]
    last_k = None
    suit = None
    current_index = 0
    number = None
    current_suit = None
    current_number = None
    tile = None
    discard_from = 'wall'
    actions = {
            '/': "discard from wall",
            '.': "move to hand",
            ',': "discard from hand",
    }
    action_key = ','
    while True:
        
        k = command_window.getkey()
        
        if k == 'KEY_RESIZE':
            continue

        if ord(k) == 10:
            # Enter key = execute action

            if action_key == '/':
                if wall.pull(tile):
                    discards.add(tile)
                #else:
                #    raise Exception("tile {} was not there".format(tile))

            if action_key == '.':
                if wall.pull(tile):
                    hand.add(tile)
                #else:
                #    raise Exception("tile {} was not there".format(tile))

            if action_key == ',':
                if hand.pull(tile):
                    discards.add(tile)
                #else:
                #    raise Exception("tile {} was not there".format(tile))

            wall_window.clear()
            discard_window.clear()
            hand_window.clear()
            print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
            print_tiles(discard_window, discards.tiles, discards.last_tile)
            print_tiles(hand_window, hand.tiles, hand.last_tile)
        elif k == ".":
            action_key = '.'
        elif k == "/":
            action_key = '/'
        elif k == "p":
            # discard last tile from hand
            if hand.last_tile:
                tile = hand.pull(hand.last_tile)
                discards.add(tile)
                wall_window.clear()
                discard_window.clear()
                hand_window.clear()
                print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
                print_tiles(discard_window, discards.tiles, discards.last_tile)
                print_tiles(hand_window, hand.tiles, Tile(Suit.NONE))
        elif k == ",":
            action_key = ','
        elif k == " ":
            # pull random tile from wall
            tile = wall.draw()
            hand.add(tile)

            wall_window.clear()
            discard_window.clear()
            hand_window.clear()
            print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
            print_tiles(discard_window, discards.tiles, discards.last_tile)
            print_tiles(hand_window, hand.tiles, hand.last_tile)

        elif k == 'd':
            if last_k != 'd':
                current_index = 0
            else:
                current_index += 1
            idx = current_index % 3
            suit = dragons[idx]
            tile = Tile(suit, None)
            last_k = 'd'
        elif k == 'w':
            if last_k != 'w':
                current_index = 0
            else:
                current_index += 1
            idx = current_index % 4
            suit = winds[idx]
            tile = Tile(suit, None)
            last_k = 'w'
        elif k == 'f':
            if last_k != 'f':
                tile = Tile(Suit.FLOWER)
                last_k = 'f'
            
        else:
            try:
                number = int(k)
                if last_k != number:
                    current_index = 0
                else:
                    current_index += 1
                last_k = number

                idx = current_index % 3
                suit = num_suits[idx]
                tile = Tile(suit, number)
            except:
                pass
                    
        command_window.clear()
        command_window.addstr(0, 0, "key: {}".format(ord(k)))
        command_window.addstr(1, 0, "{}: {}".format(actions[action_key], tile))
        command_window.refresh()
        wall_window.refresh()
        hand_window.refresh()
        discard_window.refresh()

        #a = stdscr.getch()
#        curses.echo()
        # get string needs a return
        #s = stdscr.getstr(0,0, 10)
        
        #stdscr.addstr(i, 0, 'Got string {}.format(s)'.format(s))
        #a = stdscr.getch()
        #stdscr.addstr(20,5, "Got Char {} RED ALERT!".format(a), curses.color_pair(1))
        #win.addstr(0,0, "Got Char {} wBVLUEED ALERT!".format(a), curses.color_pair(2))

#        win.refresh()
 #       stdscr.refresh()
        #stdscr.getkey()

wrapper(main)
