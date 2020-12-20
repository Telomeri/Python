class Card():
    
    def __init__(self,string):
        self.card = self.create_card(string)

    def create_card(self,card):
        #First value is nation, second value in hand, third in board
        card = [card[0],card[1],0]
        if card[0] == "s":
            card[0] = "ruutu"
            if card[1] == "t":
                card[1] = 16
                card[2] = 10
                return card
            return self.value_card(card)
        elif card[0] == "h":
            card[0] = "hertta"
            return self.value_card(card)
        elif card[0] == "r":
            card[0] = "risti"
            return self.value_card(card)
        elif card[0] == "p":
            card[0] = "pata"
            if card[1] == "2":
                card[1] = 15
                card[2] = 2
                return card 
            return self.value_card(card)
        else:
            print("Error in cardnation")
    
    def value_card(self,card):
        #Getting cardvalue from "ordinary" cards
        if card[1] == "a":
            card[1] = 14
            card[2] = 1
        elif card[1] == "k":
            card[1] = card[2] = 13
        elif card[1] == "q":
            card[1] = card[2] = 12
        elif card[1] == "j":
            card[1] = card[2] = 11
        elif card[1] == "t":
            card[1] = card[2] =  10
        elif 2 <= int(card[1]) <= 9:
            card[1] = card[2] = int(card[1])
        else:
            print("error in cardvalue")
        return card
    
    def return_card(self):
        Card = []
        Card.append(self.card[0]), Card.append(self.card[1]), Card.append(self.card[2])
        return Card