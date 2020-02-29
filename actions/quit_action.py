from actions import GameAction
import sys

class QuitAction(GameAction):

    def __init__(self):
        super().__init__()
        pass

    def __str__(self):

        return "Quit?"
        
    def execute(self):
        sys.exit(1)

    def undo(self):
        pass

    def clone(self):
        None

