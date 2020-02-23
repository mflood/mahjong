import random
import enum
from wall import Wall
from suit import Suit
from tile import Tile
from hand import Hand


class InvalidTileException(Exception):
    pass

class Player():

    def __init__(self, name):
        self.name = name
        self.game = None
        self.hand = []
        self.melds = []
        self.flowers = []

    def set_game(self, game):
        self.game = game

    def draw(self, wall, count):
        
        if size < 12:
            wall.take_tiles(count=4)
        elif size == 12:
            wall.take_tiles(count=1)
        else:
            raise FullHandException


class Game():

    def __init_(self, players, wall, discard_pile):
        self.players  = players
        self.wall = wall
        self.discard_pile = discard_pile

    def add_player(self, player):
        self.players.append(player)
        player.set_game(self)
    

#    g = Game(players=[p1, p2, p3, p4], wall=wall)



def get_action_id():
    print("""
    t: set tile
    p: other player adds to discard pile
    h: add to hand
    d: discard from hand
    p: show probability of getting tile
    """)
    action = None
    while action not in ['t', 'p', 'h', 'd', 'p']:
        action = input("Enter command:")
    return action


def convert_input_to_tile(input_value):

    c_1 = input_value[0]
    number = None

    try:
        number = int(c_1)
        suit = Suit.CRAK
        return Tile(suit=suit, number=number)
    except:
        pass

    if c_1 == 'd':
        suit = Suit.DOT
        number = int(input_value[1])
    elif c_1 == 'b':
        suit = Suit.BAM
        number = int(input_value[1])
    elif c_1 == 'c':
        suit = Suit.CRAK
        number = int(input_value[1])
    elif c_1 == 'f':
        suit = Suit.FLOWER

    elif input_value == 'ww':
        suit = Suit.WEST_WIND
    elif input_value == 'ee':
        suit = Suit.EAST_WIND
    elif input_value == 'nn':
        suit = Suit.NORTH_WIND
    elif input_value == 'ss':
        suit = Suit.SOUTH_WIND

    elif input_value == 'g' or input_value == 'gd':
        suit = Suit.GREEN_DRAGON
    elif input_value == 'r' or input_value == 'rd':
        suit = Suit.RED_DRAGON
    elif input_value == 'w' or input_value == 'wd':
        suit = Suit.WHITE_DRAGON
    else:
        raise InvalidTileException()

    tile = Tile(suit=suit, number=number)
    return tile


def get_tile():
    pairs = [
        ('D1-9', 'Dot'),
        ('B1-9', 'Bamboo'),
        ('C1-9', 'Character'),
        ('nn ee ss ww', 'Wind'),
        ('w r g', 'Dragon'),
        ('F', 'Flower'),
    ]

    for item in pairs:
        print(f'{item[0]} {item[1]}')

    tile_id= input("Enter tile:")

    tile = convert_input_to_tile(tile_id)
    return tile


if __name__ == "__main__":

    """
    p: show probability of getting tile
"""

    wall = Wall()
    wall.load_tiles()

    hand = Hand()

    tile = None
    while (True):
        
        print(">>> tile is {}".format(tile))
        print(">>> hand is {}".format(hand))
        if not tile:
            tile = get_tile()
            print("got tile {}".format(tile))

        action_id = get_action_id()
        print("Got action {}".format(action_id))
        if action_id == 't':
            tile = get_tile()
        elif action_id == 'h':
            hand.add(tile)
        elif action_id == 'd':
            hand.discard(tile)
       


#action = get_action()
#tile = get_tile()
#print("Got action '{}'".format(action))


# Convert user input to a tile

# Game - shuffle wall, show next tile, player needs to type the keyboard command for the tile input


# Start


