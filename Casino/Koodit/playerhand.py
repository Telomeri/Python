from deck import Deck
from card import Card
class PlayerHand():
    
    #most complicated file yet
    def __init__(self,board):
        self.hand = []
        self.points = [0,0,0] #1st gamepoints, second cardamount points, last spadepoints
        self.board = board;
        
    def set_hand(self,deck):
        #fills the hand depending on amount of cards you already have
        i = len(self.hand)
        while i < 4:
            self.hand.append(deck.deck[0])
            deck.remove_card(deck.deck[0])
            i += 1
    
    def draw_card(self,deck):
        self.hand.append(deck.deck[0])
        deck.remove_card(deck.deck[0])
        
    def clear_hand(self):
        self.hand = []
                
    def remove_card(self,card):
        self.hand.remove(card)
        
    def return_hand(self):
        return self.hand
    
    def PlayerLegalMove(self,handcard,boardcards):
        holderboard = self.board.board.copy()
        i = 0
        exitnum = 0
        combo = len(boardcards)
        if handcard in self.hand:
            while exitnum != combo:
                #if only one card, and is there for 3 card combos
                if combo == 3 and len(boardcards[0]) != 3:
                    total = 0
                    while i != combo:
                        total += boardcards[2]
                        i += 1
                    if combo == i:
                        return True
                    else: 
                        return False
                #if card in board, adds one card to total cards needed for "combo
                elif boardcards[i] in holderboard:
                    holderboard.remove(boardcards[i])
                    i += 1
                #when i reaches the combo amount, returns either true or false
                if i == combo:
                    i = 0
                    total = 0
                    while i != combo:
                        total += boardcards[i][2]
                        i += 1
                    if handcard[1] == total:
                        return True
                    else: 
                        return False
                else:
                    #making sure this doesn't fail if the cards are in "wrong order" for algorithm
                    exitnum += 1            
        return False
                    
    def playermoveinput(self,guicards,newboard):
        playermoves = []
        self.board = newboard
        handcard = guicards[0]
        boardcards = []
        boardcardamount = len(guicards)-1
        i = 0
        #takes input untill you hit enter on empty space
        while i < boardcardamount:
            boardcards.append(guicards[i+1])
            i += 1
        playermoves.append(handcard)
        playermoves.append(boardcards)
            #if playerlegalmove return true, deletes cards from the board and hand, and returns
            #the cards you used. Not sure if needed
        if self.PlayerLegalMove(playermoves[0], playermoves[1]):
            counter = 0
            while (counter != len(playermoves[1])):
                self.board.board.remove(playermoves[1][counter])
                counter += 1
            self.hand.remove(playermoves[0])
            if self.board.board == []:
                self.add_gamepoints(1)
            return self.countpointscard(guicards)
        else:
            return False
        
    def countpointscard(self,cards):
        i = 0
        while(i < len(cards)):
            card = cards[i]
            if card[2] == 1:
                self.add_gamepoints(1)
            if card[0] == 'pata':
                self.add_spadepoints(1)
            if card[1] == 16:
                self.add_gamepoints(2)
            if card[1] == 15:
                self.add_gamepoints(1)
            i += 1
        return i
        
    def add_gamepoints(self, points):
        self.points[0] += points
    
    def add_roundpoints(self,points):
        self.points[1] += points
        
    def add_spadepoints(self,points):
        self.points[2] += points
        
        
        