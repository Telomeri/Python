from playerhand import PlayerHand
from deck import Deck
from board import Board

#Player class take takes advantage of pre-existing classes, so looks decent
class Player():

    def __init__(self,playernumber):
        self.playernumber = playernumber
        self.playerhand = []     
        
    def set_playerhand(self,deck,board):
        #if then hand is empty, creates it, otherwise just fills the hand.
        if self.playerhand == []:
            self.playerhand = PlayerHand(board)
        self.playerhand.set_hand(deck)
        
    def set_playernumber(self,playernumber):
        self.playernumber = playernumber
    
    def player_move(self):
        playermove = self.playerhand.playermoveinput()
    
    def return_playerhand(self):
        return self.playerhand.return_hand()
    
    def add_playerhand(self,hand):
        self.playerhand = hand
            
        
        
            