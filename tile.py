
class Tile():

    def __init__(self, suit, number=None):
        self.suit = suit
        self.number = number

    def __repr__(self):
        return "Tile({}, {})".format(self.suit, self.number)

    def __str__(self):
        suit = str(self.suit).replace("Suit.", "")

        if self.number:
            return "|{} {}|".format(suit, self.number)
        else:
            return "|{}|".format(suit)

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



