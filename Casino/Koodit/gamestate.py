from deck import Deck  
from board import Board
from player import Player
from newgame import NewGame

class GameState():
    
    def __init__(self,gui):
        self.gui = gui
        self.setupGame()
        
        
    def setupGame(self):
        self.gui.consoletext.append("Welcome to the Kasino!\n")
        self.gui.consoletext.append("First, choose which of the options of the game you would like to run.\n")
        self.gui.buttonChoices()
    
    def newGame(self, GameInformation):
        self.players = GameInformation[0]
        self.board = GameInformation[1]
        self.deck = GameInformation[2]
        self.gui.createCards(self.deck,self.board,self.players)
    