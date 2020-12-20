from card import Card
from presetcards import PresetCards
#this class creates the deck using Card and PresetCards classes. Draws already shuffled list of strings
#and adds card properties to each one
class Deck():
    
    def __init__(self):
        self.deck = self.get_preset()
        
    def get_preset(self):
        presetcards1 = PresetCards()
        self.deck = presetcards1.presetcards
        self.deck = self.make_deck()
        return self.deck
    
    def make_deck(self):
        i = 0
        while i < len(self.deck):
            singlecard = Card(self.deck[i])
            self.deck[i] = singlecard.card
            i += 1
        return self.deck
            
    def return_deck(self):
        return self.deck
        
    def remove_card(self,card):
        self.deck.remove(card)
    
    def add_deck(self,deck):
        self.deck = deck