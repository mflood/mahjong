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
from actions import WallToDiscardAction
from actions import WallToHandAction
from actions import HandToDiscardAction
from actions import RandomFromWallToHandAction
from actions import HandLastTileToDiscardAction
from actions.chow_action import ChowAction
from actions.pung_action import PungAction
from actions.quit_action import QuitAction

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

    action_object = WallToDiscardAction(wall, discards, tile)

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
            action_list.append(action_object)
            action_object = action_object.clone()
            if not action_object:
                action_object = WallToDiscardAction(wall, discards, tile) 

            print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
            print_tiles(discard_window, discards.tiles, discards.last_tile)
            print_tiles(hand_window, hand.tiles, hand.last_tile)
            print_hand_block(hand_block_window, hand, wall)

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
                print_hand_block(hand_block_window, hand, wall)
            except IndexError:
                pass
        elif k == ".":
            action_object = WallToHandAction(wall, hand, tile)
        elif k == "/":
            action_object = WallToDiscardAction(wall, discards, tile)
        elif k == "q":
            action_object = QuitAction()
        elif k == ",":
            action_object = HandToDiscardAction(hand, discards, tile)
        elif k == "]":
            if isinstance(action_object, ChowAction):
                action_object.toggle_mode()
            else:
                action_object = ChowAction(wall, hand, discards)
        elif k == "\\":
            if isinstance(action_object, PungAction):
                action_object.toggle_mode()
            else:
                action_object = PungAction(wall, hand, discards)
        elif k == "p":
            # pass
            # discard last tile from hand
            if hand.last_tile:
                discard_last_action = HandLastTileToDiscardAction(hand, discards)
                discard_last_action.execute()
                action_list.append(discard_last_action)

                print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
                print_tiles(discard_window, discards.tiles, discards.last_tile)
                print_tiles(hand_window, hand.tiles, hand.last_tile)
                print_hand_block(hand_block_window, hand, wall)

        elif k == " ":
            # pull random tile from wall
            pull_action = RandomFromWallToHandAction(wall, hand)
            pull_action.execute()
            action_list.append(pull_action)

            print_tiles(wall_window, wall.tiles, Tile(Suit.NONE))
            print_tiles(discard_window, discards.tiles, discards.last_tile)
            print_tiles(hand_window, hand.tiles, hand.last_tile)
            print_hand_block(hand_block_window, hand, wall)

        elif k == 'd':
            # toggle dragon
            dragons = [Suit.GREEN_DRAGON, Suit.WHITE_DRAGON, Suit.RED_DRAGON]
            if tile.suit in dragons:
                location = dragons.index(tile.suit)
                location += 1
                location %= len(dragons)
            else:
                location = 0
            tile = Tile(dragons[location])
            action_object.tile = tile

        elif k == 'w':
            # toggle wind
            winds = [Suit.NORTH_WIND, Suit.SOUTH_WIND, Suit.EAST_WIND, Suit.WEST_WIND]
            if tile.suit in winds:
                location = winds.index(tile.suit)
                location += 1
                location %= len(winds)
            else:
                location = 0
            tile = Tile(winds[location])
            action_object.tile = tile

        elif k == 'f':
            tile = Tile(Suit.FLOWER)
            action_object.tile = tile
            
        else:
            try:
                normals = [Suit.BAM, Suit.CRAK, Suit.DOT]
                number = int(k)
                if number < 1 or number > 9:
                    continue
                location = 0
                if tile.number == number:
                    if tile.suit in normals:
                        location = normals.index(tile.suit)
                        location += 1
                        location %= len(normals)
                    else:
                        location = 0

                tile = Tile(normals[location], number)
                action_object.tile = tile

            except:
                pass
                    

wrapper(main)
