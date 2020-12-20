import random

class PresetCards():
    #this class automatically shuffles the deck, so no need for it in deck
    def __init__(self):
        self.presetcards = self.get_preset()
        
    def get_preset(self):
        self.presetcards2 = ["sa","s2","s3","s4","s5","s6","s7","s8","s9","st","sj","sq","sk",
                            "ha","h2","h3","h4","h5","h6","h7","h8","h9","ht","hj","hq","hk",
                            "ra","r2","r3","r4","r5","r6","r7","r8","r9","rt","rj","rq","rk",
                            "pa","p2","p3","p4","p5","p6","p7","p8","p9","pt","pj","pq","pk",]
        self.presetcards = self.presetcards2.copy()
        random.shuffle(self.presetcards)
        return self.presetcards
    
    def return_preset(self):
        return self.presetcards
        
        
    