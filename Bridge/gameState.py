'''
Created on Sep 24, 2015

@author: bpeterso
'''
#from wx.tools.Editra.src.extern.pygments.lexers import other
#from pip._vendor.distlib._backport.tarfile import LENGTH_LINK


import random
import datetime

_TEXT_SHORT_RANK = ['2','3','4','5','6','7','8','9','T','J','Q','K','A','Joker']
_TEXT_SHORT_SUIT = ['C','D','H','S']


def str_short_rank(rank):
    return _TEXT_SHORT_RANK[rank]

def str_short_suit(suit):
    return _TEXT_SHORT_SUIT[suit]

class Card(object):
    '''
    classdocs
    '''
    
    def __init__(self, ID, nRanks, nSuits, nJokers):
        'Perhaps jokers should be a fifth suit?'
        self.value = ID
        self._ranks = nRanks
        self._ranks = nSuits
        self._jokers = nJokers
        self.trump = False
        
        
    def set_trump_state(self, suit):
        'Tip: use suit=-1 for no trump suit'
        self.trump = self.suit() == suit
        
    def rank(self):
        return self.value // self._ranks
    
    def suit(self):
        return self.value % self._ranks
    
    def __str__(self):
        return _TEXT_SHORT_RANK[self.rank()] + _TEXT_SHORT_SUIT[self.suit()]
    
    def __cmp__(self, other):
        return self.cmp_rank_first(other)

    def __lt__(self, other): #python 3.0
        return (self.cmp_rank_first(other) < 0) 

    def __eq__(self, other): #python 3.0
        return self.cmp_rank_first(other) == 0
        
    def cmp_play(self, other):
        "Trump suit comparison, possibly overwrite for other card games"
        if self.suit() == other.suit():
            return self.rank() - other.rank()
        if other.trump:
            return -1
        return 1
        
    def cmp_suit_first(self, other):
        "Trump suit comparison, possibly overwrite for other card games"
        if self.suit() == other.suit():
            return self.rank() - other.rank()
        return self.suit() - other.suit()
    
    def cmp_rank_first(self, other):
        "Trump suit comparison, possibly overwrite for other card games"
        if self.rank() == other.rank():
            return self.suit() - other.suit()
        return self.rank() - other.rank()


class Deck(object):
    
    def __init__(self, nRanks = 13, nSuits = 4, nJokers = 0):
        numCards = nRanks * nSuits +  nJokers
        self.stack = []
        self.topCard = 0
        for cardVal in range(numCards):
            self.stack.append(Card(cardVal, nRanks=nRanks, nSuits=nSuits, nJokers=nJokers))
            
    def shuffle(self):
        random.shuffle(self.stack)
        
    def set_trump(self, trumpSuit):
        map(lambda x: x.set_trump_state(trumpSuit), self.stack)
        
    def deal(self, numCards, numHands):
        deal = []
        for hand in range(numHands):
            deal.append([])
        for count in range(numCards):
            for hand in range(numHands):
                if self.topCard + 1 > len(self.stack):
                    return deal
                card = self.stack[self.topCard]
                deal[hand].append(card)
                self.topCard += 1
        return deal
    
    def __str__(self):
        return ' '.join(map(str, self.stack))
        

class CardArray(object):
    
    def __init__(self, cards=[]):
        self.hand = cards
        self.suits = [0,1,2,3]
        self._suitDisplayOrder = [3,2,1,0]
        
    def add_card(self,card):
        self.cards.append(card)

    def play_card(self, card):
        self.cards.remove(card)
        return card
        
    def get_sorted_cards(self):
        'Returns a dictionary of suits lists cards '
        pass

    def __str__(self):
        result = ''
        suitedHand = self.sort_hand_by_suits()
        for suit in self._suitDisplayOrder:
            result += str_short_suit(suit)+':'
            for card in suitedHand[suit]:
                result += str_short_rank(card.rank())
            result += ' '
        return result
                
    def _str_evaluation(self):
        result = ''
        suitLens = []
        for suit in self._suitDisplayOrder:
            suitLens.append(self.len_suits()[suit])
        result += '-'.join(map(str,suitLens)) + ' '
        result += str(self.evaluation())
        return result

    def len_suits(self):
        suitLengths = {}
        result = []
        for suit in self.suits:
            suitLengths[suit] = 0
        for card in self.hand:
            if card.suit() in self.suits:
                suitLengths[card.suit()] += 1
        for suit in self.suits:
            result.append(suitLengths[suit])
        return result
    
    def evaluation(self):
        return sum(map(lambda x: max(0, x.rank() - 8), self.hand))

    def sort_hand_by_suits(self):
        sortedHand = {}
        for suit in self.suits:
            sortedHand[suit] = []
        for card in self.hand:
            if card.suit() in self.suits:
                sortedHand[card.suit()].append(card)
        for suit, cardsInSuit in sortedHand.items():
            cardsInSuit.sort(reverse=True)
        return sortedHand
        




class BridgeGameState(object):
    '''
    classdocs
    
    Describes a tournament game state
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._VUL_TEXT = ['None','NS', 'EW', 'Both']
        self._DEALER_TEXT = ['N', 'E', 'S', 'W']
        self.players = ['', '', '', '']
        self.boardID = 0
        self.vunerability = 0
        self.dealer = 0
        self.cards = Deck(nRanks = 13, nSuits = 4, nJokers = 0) 
        self.north = CardArray()
        self.east = CardArray()
        self.south = CardArray()
        self.west = CardArray()
        self.auction = []
        self.cardsOnThefloor = []
        self.listeners = []
        self.lastCommunication = datetime.datetime.now()
        self.turn = 0
        self.currentBidLevel = -1
        self.lastCaller = -1
        self.doubleLevel = 0
        
    def bid_box_choice(self):
        levels = range(7)
        suits = range(5)
        other = range(3) #pass, double/redouble
        alert = range(2)
    
    def bid_phase(self):
        print ("communicate with player", self.turn)
        input("What's your bid")
        while True:
            numPasses = 0
            while numPasses < 4 :
                # bid = get_bid()
                pass
        
    def play(self):
        self.bid_phase()
        
    
    def update_status(self):
        for listener in self.listeners:
            listener.talk()
            
    def suffle_deal(self):
        self.cards.shuffle()
        deals = self.cards.deal(13, 4)
        self.north, self.east, self.south, self.west = map(CardArray, deals)
        
    def _str_show_table(self):
        "technically as an external display procedure, I guess"
        result = ''
        result += '  Board: ' + str(self.boardID) + '\n'
        result += '    Vul: ' + self._VUL_TEXT[self.vunerability] + '\n'
        result += 'Players: ' + ', '.join(self.players) + '\n'
        nsFmtStr = ' '*12+'{:25}\n'+' '*12+'{:25}\n'
        ewFmtStr = '{:25}'+' '*12+'{:25}\n'
        result += nsFmtStr.format(str(self.north), self.north._str_evaluation())
        result += ewFmtStr.format(str(self.west), str(self.east))
        result += ewFmtStr.format(self.west._str_evaluation(), self.east._str_evaluation())
        result += nsFmtStr.format(str(self.south), self.south._str_evaluation())
        return result
    
if __name__ == '__main__':
    deck = Deck()
    deck.shuffle()
    print (deck) 
    table = []
    for hand in deck.deal(13, 4):
        table.append(CardArray(hand))
    for i, hand in enumerate(table):
        print (i, hand)
    game = BridgeGameState()
    game.suffle_deal()
    print (game._str_show_table())
    
    game.play()
        