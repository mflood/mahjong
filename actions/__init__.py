import copy

from tile_chooser import TileChooser

class ActionException(Exception):
    pass

class GameAction():

    def __init__(self):
        pass

    def toggle(self, reverse=False, tab=False):
        pass

    def handle_key(self, k):
        pass
