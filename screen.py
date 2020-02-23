from curses import wrapper
import curses
import time
from wall import Wall
from hand import Hand
import random
from tile import Tile

from suit import Suit
from discards import Discards

from tile_window import print_tiles
from actions import WallToDiscardAction
from actions import WallToHandAction
from actions import HandToDiscardAction
from actions import RandomFromWallToHandAction

def main(stdscr):
    
    action_list = []

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
    tile = Tile(Suit.BAM, 1)
    discard_from = 'wall'
    actions = {
            '/': "discard from wall",
            '.': "move to hand",
            ',': "discard from hand",
    }
    action_key = ','

    action_object = WallToDiscardAction(wall, discards, tile)

    while True:
        
        command_window.clear()
        command_window.addstr(1, 0, "{}".format(action_object))
        command_window.refresh()
        wall_window.refresh()
        hand_window.refresh()
        discard_window.refresh()

        k = command_window.getkey()
        command_window.addstr(0, 0, "key: {}".format(ord(k)))
        command_window.refresh()
        
        if k == 'KEY_RESIZE':
            continue

        if ord(k) == 10:
            # Enter key = execute action

            action_object.execute()
            action_list.append(action_object)
            action_object = action_object.clone()

            print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
            print_tiles(discard_window, discards.tiles, discards.last_tile)
            print_tiles(hand_window, hand.tiles, hand.last_tile)

        elif k == "u":
            try:
                last_action = action_list.pop()
                last_action.undo()
                replace_action_object = last_action.clone()
                if replace_action_object:
                    action_object = replace_action_object

                print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
                print_tiles(discard_window, discards.tiles, discards.last_tile)
                print_tiles(hand_window, hand.tiles, hand.last_tile)
            except IndexError:
                pass
        elif k == ".":
            action_key = '/'
            action_object = WallToHandAction(wall, hand, tile)
        elif k == "/":
            action_key = '/'
            action_object = WallToDiscardAction(wall, discards, tile)
        elif k == ",":
            action_key = ','
            action_object = HandToDiscardAction(hand, discards, tile)
        elif k == "p":
            # discard last tile from hand
            if hand.last_tile:
                tile = hand.pull(hand.last_tile)
                if action_object:
                    action_object.tile = tile

                discards.add(tile)
                wall_window.clear()
                discard_window.clear()
                hand_window.clear()
                print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
                print_tiles(discard_window, discards.tiles, discards.last_tile)
                print_tiles(hand_window, hand.tiles, Tile(Suit.NONE))
        elif k == " ":
            # pull random tile from wall
            pull_action = RandomFromWallToHandAction(wall, hand)
            pull_action.execute()
            action_list.append(pull_action)

            print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
            print_tiles(discard_window, discards.tiles, discards.last_tile)
            print_tiles(hand_window, hand.tiles, hand.last_tile)

        elif k == 'd':
            # toggle dragon
            if last_k != 'd':
                current_index = 0
            else:
                current_index += 1
            idx = current_index % 3
            suit = dragons[idx]
            tile = Tile(suit, None)
            if action_object:
                action_object.tile = tile
            last_k = 'd'
        elif k == 'w':
            if last_k != 'w':
                current_index = 0
            else:
                current_index += 1
            idx = current_index % 4
            suit = winds[idx]
            tile = Tile(suit, None)
            if action_object:
                action_object.tile = tile
            last_k = 'w'
        elif k == 'f':
            if last_k != 'f':
                tile = Tile(Suit.FLOWER)
                if action_object:
                    action_object.tile = tile
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
                if action_object:
                    action_object.tile = tile
            except:
                pass
                    

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
