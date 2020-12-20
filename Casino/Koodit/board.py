from deck import Deck

class Board():
    
    def __init__(self):
        self.board = []
        
    def set_board(self,deck):
        #creates board with 4 cards
        if self.board == []:
            i = 0
            while i < 4:
                self.board.append(deck.deck[0])
                deck.remove_card(deck.deck[0])
                i += 1
    
    def draw_card(self,deck):
        if len(self.board) < 12:
            self.board.append(deck.deck[0])
            deck.remove_card(deck.deck[0])
        
    def remove_card(self,card):
        self.board.remove(card)
        
    def return_board(self):
        return self.board
    
    def add_board(self,board):
        self.board = board
                
        