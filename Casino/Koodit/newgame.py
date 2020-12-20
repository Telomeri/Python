from deck import Deck  
from board import Board
from player import Player


class NewGame():
    
    def __init__(self,gui):
        self.gui = gui
        self.new()
        
    def new(self):
        self.gui.consoletext.append("You chose to create new game\n")
        self.board = Board()
        self.gui.consoletext.append("Lets start off by shuffling our deck\n")
        self.deck = Deck()
        self.gui.consoletext.append("How many players will be playing? \n")
        self.board.set_board(self.deck)
        self.gui.playerAmount()

           
    def set_players(self, amount, game):
        self.players = []
        i = 1
        while (i <= amount):
            player = Player(i)
            player.set_playerhand(self.deck,self.board)
            self.players.append(player)
            i += 1
        self.gui.consoletext.append("Now lets place the cards on the board")
        game.newGame([self.players,self.board,self.deck])
            
               
        

        
    
            
               
        
    