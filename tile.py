from suit import Suit

class Tile():

    def __init__(self, suit, number=None):
        self.suit = suit
        self.number = number

    def __repr__(self):
        return "Tile({}, {})".format(self.suit, self.number)

    def __hash__(self):
        return hash(str(self))

    def long_name(self):

        if self.suit == Suit.FLOWER:
            return "FLOWER"

        if self.suit == Suit.EAST_WIND:
            return "East Wind"
        if self.suit == Suit.WEST_WIND:
            return "West Wind"
        if self.suit == Suit.NORTH_WIND:
            return "North Wind"
        if self.suit == Suit.SOUTH_WIND:
            return "South Wind"

        if self.suit == Suit.GREEN_DRAGON:
            return "Green Dragon"
        if self.suit ==Suit.RED_DRAGON:
            return "Red Dragon"
        if self.suit == Suit.WHITE_DRAGON:
            return "White Dragon"

        if self.suit == Suit.BAM:
            return "{} Bamboos".format(self.number)
        if self.suit == Suit.CRAK:
            return "{} Characters".format(self.number)
        if self.suit == Suit.DOT:
            return "{} Dots".format(self.number)

        return "??"
        pass
        

    def __str__(self):

        if self.suit == Suit.FLOWER:
            return "{*}"

        if self.suit == Suit.EAST_WIND:
            return "Ee)"
        if self.suit == Suit.WEST_WIND:
            return "Ww)"
        if self.suit == Suit.NORTH_WIND:
            return "Nn)"
        if self.suit == Suit.SOUTH_WIND:
            return "Ss)"

        if self.suit == Suit.GREEN_DRAGON:
            return "-G->"
        if self.suit ==Suit.RED_DRAGON:
            return "-R->"
        if self.suit == Suit.WHITE_DRAGON:
            return "-W->"

        if self.suit == Suit.BAM:
            return "!{}".format(self.number)
        if self.suit == Suit.CRAK:
            return "#{}".format(self.number)
        if self.suit == Suit.DOT:
            return "o{}".format(self.number)

        return "??"

    def __eq__(self, other):
        return ((int(self.suit), self.number) == (int(other.suit), other.number))

    def __ne__(self, other):
            return ((self.suit, self.number) != (other.suit, other.number))

    def __lt__(self, other):
        return ((self.suit, self.number) < (other.suit, other.number))

    def __lt__(self, other):
        return ((int(self.suit), self.number) < (int(other.suit), other.number))

    def __le__(self, other):
        return ((self.suit, self.number) <= (other.suit, other.number))

    def __gt__(self, other):
        return ((self.suit, self.number) > (other.suit, other.number))

    def __ge__(self, other):
        return ((self.suit, self.number) >= (other.suit, other.number))



