from actions import GameAction

class RandomFromWallToHandAction(GameAction):

    def __init__(self, wall, hand):
        super().__init__()
        self.wall = wall
        self.hand = hand

        # for undo state
        self._wall_state = None
        self._hands_state = None

    def __str__(self):
        return "Random Wall to Hand: {}".format(self.tile.long_name())

    def execute(self):

        self._wall_state = self.wall.get_state()
        self._hands_state = self.hand.get_state()


        while(self.hand.hand_size() < 14): 
            tile = self.wall.draw()
            if tile:
                self.hand.add(tile)
            else:
                break

    def undo(self):
        self.wall.set_state(self._wall_state)
        self.hand.set_state(self._hands_state)
    
    def clone(self):
        return None

