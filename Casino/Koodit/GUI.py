from PyQt5 import QtCore, QtWidgets
import sys
from PyQt5.Qt import QRect, Qt, QPainter, QPen, QSize, QColor, QPoint
from PyQt5.QtGui import QPainter, QBrush, QPen, QResizeEvent
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QGraphicsScene, QGraphicsView, QGraphicsItem, QDialog
    
from card import Card 
from deck import Deck  
from board import Board
from gamestate import GameState
from newgame import NewGame
from functools import partial
from savegame import SaveGame

        

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent) #tekee ikkunan
        self.gamecreated = False
        self.turntimer = 1
        self.setGeometry(QRect(350,100,900,900))
        self.setWindowTitle("Kasino")
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.initUI()
        self.show()
    
    def initUI(self):    
        self.console() #tekee ui:n aluksi
        self.bootGame()
        self.deckLayout()
        self.boardLayout(False)
        self.handLayout(False)
        
    def bootGame(self):
        self.bootgame = QPushButton('Start Game',self)
        self.bootgame.clicked.connect(self.Game) #aloittaa pelin
        self.bootgame.move(175, 775)
        self.bootgame.resize(200, 50)
        self.bootgame.setStyleSheet("background-color: rgb(170, 175, 58)")
        
    def createCards(self,deck,board,players):
        self.consoletext.append("New round starts") #luo pelin
        self.movelegalcheck = []
        self.passertimer = 50
        self.deckvalues = deck
        self.boardvalues = board
        self.playervalues = players
        self.savegame = QPushButton("Save Game",self)
        self.savegame.move(25, 25)
        self.savegame.resize(100, 50)
        self.savegame.clicked.connect(partial(self.save_game,self.deckvalues,self.boardvalues,self.playervalues))
        self.savegame.show()
        self.updateGUI()
        self.cardraw = QPushButton('Draw Card',self)
        self.cardraw.clicked.connect(self.drawCard)
        self.cardraw.move(570,360)
        self.cardraw.resize(100, 50)
        self.cardraw.setStyleSheet("background-color: rgb(42, 126, 163)")
        self.cardraw.show()
        self.readybutton = QPushButton('Turn Ready',self)
        self.readybutton.clicked.connect(self.turnReady)
        self.readybutton.setDisabled(True)
        self.readybutton.move(570,190)
        self.readybutton.resize(100, 50)
        self.readybutton.setStyleSheet("background-color: rgb(42, 126, 163)")
        self.readybutton.show()
        self.turn()
        
    def save_game(self,deck,board,players): #tallentaa pelin
        SaveGame(deck,board,players)
        self.consoletext.append("Game saved")
        
    def turnReady(self):
        self.enableBoardcards(True)
        self.readybutton.setDisabled(True) #katsoo onko liike laillinen
        value = self.playervalues[self.turntimer-1].playerhand.playermoveinput(self.movelegalcheck,self.boardvalues)
        self.movelegalcheck = []
        if value ==  False:
            self.consoletext.append("Move illegal")
            self.turn()
        else:
            self.consoletext.append("Move Legal, cards taken to this turn: " + str(value) + " points to roundscore")
            self.passertimer = 50
            if len(self.deckvalues.deck) > 0:
                self.playervalues[self.turntimer-1].playerhand.set_hand(self.deckvalues)
            self.consoletext.append("New card drawn for player " + str(self.turntimer))
            self.turntimer += 1
            self.turn()
    
    def gamewinner(self):
        i = 0
        while i != len(self.playervalues): #selvittää voittajan
            if self.playervalues[i].playerhand.points[0] >= 16:
                self.consoletext.append("Player: " + str(i) + " wins! \n Congratulations!!! \n")
                self.enableBoardcards(True)
                self.readybutton.setDisabled(True)
                self.cardraw.setDisabled(True)
                return 0
            i += 1
        return 1
        
    def roundwinner(self):
        k = 0
        n = 0
        while n < len(self.playervalues):
            if (len(self.deckvalues.deck) == 0 and len(self.boardvalues.board) == 0):
                k += 1
            n += 1
        if self.passertimer == 8:
            k = len(self.playervalues) 
        if k == len(self.playervalues):
            self.deckvalues = Deck()
            self.boardvalues = Board()
            self.boardvalues.set_board(self.deckvalues)
            i = 0
            while i < len(self.playervalues):
                self.playervalues[i].playerhand.clear_hand()
                self.playervalues[i].playerhand.set_hand(self.deckvalues)
                i += 1
            self.consoletext.append("The round has ended")
            self.spadeWinner(2)
            self.spadeWinner(1)
            self.consoletext.append("Current scores:")
            self.printScores()
            if self.gamewinner() == 0:
                return 0
            if self.turntimer > len(self.playervalues):
                self.turntimer = 1
            self.consoletext.append("The new dealer is player " + str(self.turntimer))
            self.createCards(self.deckvalues, self.boardvalues, self.playervalues)    
        
    def printScores(self): #printtaa tilanteen
        i = 0
        while(i < len(self.playervalues)):
            self.consoletext.append("Player " + str(i+1) + " has " + str(self.playervalues[i].playerhand.points[0]) + " points")
            i += 1
    
    def spadeWinner(self,point): #laskee kierroksen pistevoittoja, eli eniten kortteja ja patoja
        i = 0
        winner = 0
        while(i < len(self.playervalues)):
            if winner < self.playervalues[i].playerhand.points[point]:
                winner = self.playervalues[i].playerhand.points[point]
                winningplayer = self.playervalues[i]
            i += 1
        if winner != 0:
            winningplayer.playerhand.points[0] += point
        
    def turn(self): #vastaa vuorosta 
        self.updateGUI()
        self.roundwinner()
        if self.turntimer <= len(self.playervalues):
            self.consoletext.append("Player " + str(self.turntimer) + " turn")
            self.enableHandcards(False)
        else:
            self.turntimer = 1
            self.consoletext.append("Player " + str(self.turntimer) + " turn")
            self.enableHandcards(False)
        
    def handcardButtonpress(self,value): #vastaa nappaimenpainosta, saa painetun kortin arvon
        self.enableHandcards(True)
        self.consoletext.append("Handcard chosen: " + str(self.playervalues[value[0]].playerhand.hand[value[1]]))
        self.movelegalcheck.append(self.playervalues[value[0]].playerhand.hand[value[1]])
        self.enableBoardcards(False)
        
    def boardcardButtonpress(self,value):
        self.consoletext.append("Boardcard chosen: " + str(self.boardvalues.board[value]))
        self.readybutton.setDisabled(False)
        self.movelegalcheck.append(self.boardvalues.board[value])
        
                
    def enableBoardcards(self,statement):
        i = 0
        while (i < len(self.boardvalues.board)):
            self.boardcardlist[i].setDisabled(statement)
            i += 1
            
    def enableHandcards(self,statement): #enabloi kasikortit
        player = self.turntimer
        i = 0
        while (i < len(self.playervalues[player-1].playerhand.hand)):
            self.handcardlist[i][player-1].setDisabled(statement)
            card = self.playervalues[player-1].playerhand.hand[i]
            if (self.check_Cardcolor(card) == 0):
                self.handcardlist[i][player-1].setStyleSheet("background-color: rgb(173, 33, 8); color: rgb(124, 119, 23)")
            else:
                self.handcardlist[i][player-1].setStyleSheet("background-color: rgb(48, 44, 44); color: rgb(124, 119, 23)")
            i += 1
        
    def updateGUI(self):
        self.deck_gui_update()
        self.board_gui_update()
        self.hands_gui_update()
    
    def drawCard(self): #nostaa kortin, jos 12 korttia ei tee mitaan
        if len(self.deckvalues.deck) > 0:
            self.boardvalues.draw_card(self.deckvalues)
            self.deck_gui_update()
            self.board_gui_update() 
            if len(self.boardvalues.board) == 12:
                self.consoletext.append("Too many cards on the board")
            else:
                self.turntimer += 1
                self.turn()
        else:
            self.consoletext.append("The deck is empty, passing turn")
            if self.passertimer == 50:
                self.consoletext.append("Passertimer has been activated, to disable it, make a legal move. \nOtherwise game will end in 4 turns")
                self.passertimer = 0
            self.deck_gui_update()
            self.board_gui_update() 
            self.turntimer += 1
            self.passertimer += 1
            self.turn()
        
 
    def hands_gui_update(self): #paivittaa kortit kasissa 
        i = 0
        self.handLayout(True)
        while (i < len(self.playervalues)):
            k = 0
            while k < len(self.playervalues[i].playerhand.hand):
                card = self.playervalues[i].playerhand.hand[k]
                self.handcardlist[k][i].setToolTip((str(card[0])+"\n"+"Handvalue: "+str(card[1])+"\n"+"Boardvalue: "+str(card[2])))
                if (self.check_Cardcolor(card) == 0):
                    self.handcardlist[k][i].setStyleSheet("background-color: rgb(160, 24, 85); color: rgb(0, 0, 0)")
                else:
                    self.handcardlist[k][i].setStyleSheet("background-color: rgb(86, 95, 104); color: rgb(84, 13, 132)")
                self.handcardlist[k][i].setText(str(card[0][0].upper())+str(card[2]))  
                k += 1
            i += 1
            
        
    def deck_gui_update(self): #paivittaa korttien maaran pakassa 
        self.deck.setToolTip('This is a deck of cards')
        self.deck.setStyleSheet("background-color: rgb(43, 95, 191); color: rgb(0, 0, 0)")
        self.deck.setText(str(len(self.deckvalues.deck)))
    
    def board_gui_update(self): #paivittaa laudalle kortit
        i = 0
        self.boardLayout(True)
        while (i < len(self.boardvalues.board)):
            card = self.boardvalues.board[i]
            self.boardcardlist[i].setToolTip((str(card[0])+"\n"+"Handvalue: "+str(card[1])+"\n"+"Boardvalue: "+str(card[2])))
            if (self.check_Cardcolor(card) == 0):
                self.boardcardlist[i].setStyleSheet("background-color: rgb(160, 24, 85); color: rgb(0, 0, 0)")
            else:
                self.boardcardlist[i].setStyleSheet("background-color: rgb(86, 95, 104); color: rgb(84, 13, 132)")
            self.boardcardlist[i].setText(str(card[0][0].upper())+str(card[2]))     
            i += 1
    
    def check_Cardcolor(self,card):
        if (card[0] == 'hertta' or card[0] == 'ruutu'): #tarkistaa kortin varin
            return 0
        else:
            return 1
        
    def Game(self):
        self.bootgame.deleteLater() 
        self.game = GameState(self)
        
    def newGame(self):
        self.newgame.deleteLater()
        self.loadgame.deleteLater()
        self.newgamehold = NewGame(self)
        
    def loadGame(self):
        self.consoletext.append("Sadly did not have time to add this")
    
    def paintEvent(self, event):
        painter = QPainter(self) #luo vihrean taustan
        painter.setBrush(QBrush(QColor(37, 114, 57), Qt.SolidPattern))
        painter.drawRect(0, 0, 900, 650)
        
    def deckLayout(self):
        self.deck = QPushButton('Deck',self) #asettaa pelipakan
        self.deck.setToolTip('Gamedeck')
        self.deck.setDisabled(True)
        self.deck.move(570,250)
        self.deck.resize(70,100)
        self.deck.setStyleSheet("background-color: rgb(37, 114, 57); color: rgb(37, 114, 57)")
    
        
    
    def boardLayout(self,timecall):
        i = 0
        if timecall == False:
            self.boardcardlist = []
        y = 340
        while (i < 3):
            k = 0
            x = 350 #samantyylinen kuin cardlayout, maaraa dimension ja paikan
            while(k < 4):
                if timecall == False:
                    card = self.cardlayoutalg(x, y, 40, 60, timecall)
                    card.clicked.connect(partial(self.boardcardButtonpress,(k+(i*4))))
                    self.boardcardlist.append(card)
                else:
                    self.boardcardlist[k+(i*4)] = self.cardlayoutalg(x, y, 40, 60, self.boardcardlist[k+(i*4)])
                x += 50
                k += 1
            y -= 70
            i += 1
         
    def handLayout(self,timecall):
        player = 4 
        if timecall == False:
            self.handcardlist = []
        i = 0
        y = 475 #absolute garbage algorithm, hopefully I have time to revisit this
        while i < player:
            k = 0
            if i < 2:
                x = 330
                dx = 50
                dy = 100
            if i >= 2: 
                x = 25
                y = 180
                if i >= 3:
                    x = 775
                dx = 100
                dy = 50
            cards = []
            while k < 4:
                if timecall == False:
                    card = self.cardlayoutalg(x,y,dx,dy,timecall)
                    card.clicked.connect(partial(self.handcardButtonpress,[k,i]))
                    cards.append(card)
                else:
                    self.handcardlist[k][i] = self.cardlayoutalg(x, y, dx, dy, self.handcardlist[k][i])
                if i < 2:
                    x += 60
                else:
                    y += 60
                k += 1
            i += 1
            if i < 2:
                y -= 450
            if timecall == False:
                self.handcardlist.append(cards)
                
    def cardlayoutalg(self,x,y,dx,dy, timecall):
        if timecall == False: #apukeino paikkojen tekemiseen 
            card = QPushButton('',self)
        else:
            card = timecall
        card.setToolTip('')
        card.setDisabled(True)
        card.move(x,y)
        card.resize(dx,dy)
        card.setStyleSheet("background-color: rgb(37, 114, 57); color: rgb(37, 114, 57)")
        return card
        
            
    def console(self):
        self.consoletext = QTextEdit(self) #luo konsolin, johon voi inputtaa self.consoletext.appendin avulla
        self.consoletext.move(0,650)
        self.consoletext.resize(QSize(900,250))
        self.consoletext.setStyleSheet("background-color: rgb(202, 209, 18)")
        self.consoletext.setReadOnly(True)
        self.clearbtn = QPushButton('Clear',self)
        self.clearbtn.clicked.connect(self.clear_text)
        self.clearbtn.move(675, 775)
        self.clearbtn.resize(200, 50)
        self.clearbtn.setStyleSheet("background-color: rgb(170, 175, 58)")
        
    def clear_text(self):    
        self.consoletext.clear()
    
    #the spaghetti starts here
    def buttonChoices(self):
        self.newgame = QPushButton("New Game",self) #antaa nappain vaihtoehdot
        self.newgame.move(25, 775)
        self.newgame.resize(100, 50)
        self.newgame.clicked.connect(self.newGame)
        self.newgame.show()
        self.loadgame = QPushButton("Load Game",self)
        self.loadgame.move(225, 775)
        self.loadgame.resize(100, 50)
        self.loadgame.clicked.connect(self.loadGame)
        self.loadgame.show()
        
    def playerAmount(self):
        self.p2 = QPushButton("2 Players",self) #paattaa pelaajat 
        self.p2.move(25,825)
        self.p2.resize(75,25)
        self.p2.clicked.connect(self.player2)
        self.p2.show()
        self.p3 = QPushButton("3 Players",self)
        self.p3.move(110,825)
        self.p3.resize(75,25)
        self.p3.clicked.connect(self.player3)
        self.p3.show()
        self.p4 = QPushButton("4 Players",self)
        self.p4.move(195,825)
        self.p4.resize(75,25)
        self.p4.clicked.connect(self.player4)
        self.p4.show()
    def player2(self):
        self.p2.deleteLater()
        self.p3.deleteLater()
        self.p4.deleteLater()
        self.newgamehold.set_players(2,self.game)
    def player3(self):
        self.p2.deleteLater()
        self.p3.deleteLater()
        self.p4.deleteLater()
        self.newgamehold.set_players(3,self.game)
    def player4(self):
        self.p2.deleteLater()
        self.p3.deleteLater()
        self.p4.deleteLater()
        self.newgamehold.set_players(4,self.game)
            