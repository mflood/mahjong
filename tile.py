from suit import Suit

class Tile():

    def __init__(self, suit, number=None):
        self.suit = suit
        self.number = number

    def __repr__(self):
        return "Tile({}, {})".format(self.suit, self.number)

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
            return "-Gd->"
        if self.suit == Suit.RED_DRAGON:
            return "-Rd->"
        if self.suit == Suit.WHITE_DRAGON:
            return "-Wd->"

        if self.suit == Suit.BAM:
            return "!{}!".format(self.number)
        if self.suit == Suit.CRAK:
            return "~{}~".format(self.number)
        if self.suit == Suit.DOT:
            return "o{}o".format(self.number)

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



