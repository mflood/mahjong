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
from tile_window import print_hand_block
from tile_chooser import TileChooser
from actions.wall_to_discard_action import WallToDiscardAction
from actions.wall_to_hand_action import WallToHandAction
from actions.hand_to_discard_action import HandToDiscardAction
from actions.random_from_wall_to_hand_action import RandomFromWallToHandAction
from actions.hand_last_tile_to_discard_action import HandLastTileToDiscardAction
from actions.chow_action import ChowAction
from actions.pung_action import PungAction
from actions.quit_action import QuitAction

def main(stdscr):
    
    tile_chooser = TileChooser()
    alt_tile_chooser = TileChooser()

    action_history = []

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

    hand_block_window = curses.newwin(13, 140, begin_y + 18, begin_x + 45)

    wall_window = curses.newwin(height, width, begin_y, begin_x)
    discard_window = curses.newwin(height, width, begin_y, begin_x + 45)
    hand_window = curses.newwin(height, width, begin_y + 18, begin_x)
    command_window = curses.newwin(3, 100, 2, 2)

    print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
    print_tiles(discard_window, discards.tiles, discards.last_tile)
    print_tiles(hand_window, hand.tiles, hand.last_tile)
    print_hand_block(hand_block_window, hand, wall)


    current_index = 0
    tile = Tile(Suit.BAM, 1)
    k = None
    last_error = ""

    action_object = WallToDiscardAction(wall, discards, tile_chooser)

    while True:
        
        command_window.clear()
        command_window.addstr(1, 0, "{}".format(action_object))
        if k:
            if k == 'KEY_RESIZE':
                key = k 
                the_ord = ""
            elif ord(k) == 10:
                key = "CTRL"
                the_ord = ord(k)
            else:
                key = k
                the_ord = ord(k)
            command_window.addstr(0, 0, "key: {} ord: {} {}".format(key, the_ord, last_error))

        command_window.refresh()
        wall_window.refresh()
        hand_window.refresh()
        discard_window.refresh()

        try:
            k = command_window.getkey()
        except KeyboardInterrupt:
            pass
        
        if k == 'KEY_RESIZE':
            continue

        if ord(k) == 10:
            # Enter key = execute action

            action_object.execute()
            action_history.append(action_object)
            action_object = action_object.clone()
            if not action_object:
                action_object = WallToDiscardAction(wall, discards, tile_chooser) 

            print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
            print_tiles(discard_window, discards.tiles, discards.last_tile)
            print_tiles(hand_window, hand.tiles, hand.last_tile)
            print_hand_block(hand_block_window, hand, wall)

        elif k == "u":
            try:
                last_action = action_history.pop()
                last_action.undo()
                replace_action_object = last_action.clone()
                if replace_action_object:
                    action_object = replace_action_object

                print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
                print_tiles(discard_window, discards.tiles, discards.last_tile)
                print_tiles(hand_window, hand.tiles, hand.last_tile)
                print_hand_block(hand_block_window, hand, wall)
            except IndexError:
                pass
        elif k == ".":
            action_object = WallToHandAction(wall, hand, tile_chooser)
        elif k == "/":
            action_object = WallToDiscardAction(wall, discards, tile_chooser)
        elif k == "q": # escape
            action_object = QuitAction()
        elif k == ",":
            action_object = HandToDiscardAction(hand, discards, tile_chooser)
            print_tiles(hand_window, hand.tiles, hand.last_tile)
        elif k == "C": # right arrow
            action_object.toggle()
            print_tiles(hand_window, hand.tiles, hand.last_tile)
        elif k == "D": # left arrow
            action_object.toggle(reverse=True)
            print_tiles(hand_window, hand.tiles, hand.last_tile)
        elif k == "\t": # tab
            action_object.toggle(tab=True)
            print_tiles(hand_window, hand.tiles, hand.last_tile)
        elif k == "]":
            action_object = ChowAction(wall, hand, discards)
        elif k == "\\":
            action_object = PungAction(wall, hand, discards)
        elif k == "p":
            # pass
            # discard last tile from hand
            if hand.last_tile:
                discard_last_action = HandLastTileToDiscardAction(hand, discards)
                discard_last_action.execute()
                action_history.append(discard_last_action)

                print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
                print_tiles(discard_window, discards.tiles, discards.last_tile)
                print_tiles(hand_window, hand.tiles, hand.last_tile)
                print_hand_block(hand_block_window, hand, wall)

        elif k == " ":
            # pull random tile from wall
            pull_action = RandomFromWallToHandAction(wall, hand)
            pull_action.execute()
            action_history.append(pull_action)

            print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
            print_tiles(discard_window, discards.tiles, discards.last_tile)
            print_tiles(hand_window, hand.tiles, hand.last_tile)
            print_hand_block(hand_block_window, hand, wall)

        else:
            action_object.handle_key(k)

wrapper(main)
