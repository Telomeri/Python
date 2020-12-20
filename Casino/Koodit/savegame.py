from deck import Deck  
from board import Board
from player import Player

class SaveGame():
    
    def __init__(self,deck,board,players):
        file = open("savinggame.txt", "w")
        file.write("The gamefile of Kasino\n")
        file.write(str(deck.deck))
        file.write("\n")
        file.write(str(board.board))
        file.write("\n")
        file.write(str(len(players)))
        file.write("\n")
        i = 0
        while (i < len(players)):
               file.write(str(players[i].playerhand.hand))
               file.write("\n")
               file.write(str(players[i].playerhand.points))
               file.write("\n")
               i += 1
        file.close()
        