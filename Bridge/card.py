

DEBUG = True


class trumpComparitor():

    def __init__(self):
        self.trump = None # set after bidding
        self.ledSuit = None # set at each round

    def compare(self, origCard, otherCard):
        if origCard.suit == otherCard.suit:
            if origCard.rank - otherCard.rank == 0: # e.g. Pinochle
                return 1
            return origCard.rank - otherCard.rank
        if origCard.suit == self.trump:
            return 1
        if otherCard.suit == self.trump:
            return -1
        if origCard.suit == self.ledSuit:
            return 1
        if otherCard.suit == self.ledSuit:
            return -1
        return 9999999 #Non-winner
        
            
        
class StandardCard():

    def __init__ (self, suit, rank):
        # There are 5 suits:  Clubs, Diamonds, Hearts, Spades, Jokers
        self.suit = int(suit);
        self.rank = int(rank);
        self.suit_short_label = ['C', 'D', 'H', 'S', 'Joker']
        self.rank_short_label = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q','K', 'A']
        self.suit_long_label = ['Club', 'Diamond', 'Heart', 'Spade', 'Joker']
    
    def is_joker(self):
        return self.rank == 4;
    
    def __str__(self):
        res = self.rank_short_label[self.rank] + self.suit_short_label[self.suit] 
        return res

def debug ():
    
    comparitor = trumpComparitor()

    # In a play in the table, the cards would already be delt
    def tuple_to_card(a):
        return StandardCard(a[0], a[1])


    A = [ (0,0), (0,2), (1,2), (0,3) ]
    for aSet in [A,]:

        cardPlayA = map(tuple_to_card, A )
        comparitor.ledSuit = 0
        winner =  max(cardPlayA, key=comparitor.compare)

        print("Play: ",)
        for card in cardPlayA:
            print(card);
        print()
        print("Suit: ", suit, "   Trump: ", trump)
        print("Winner: ", winner)


if __name__ == "__main__":
    print ("Not a callable module")
    if not DEBUG:
        import sys
        sys.exit(1)
    debug()