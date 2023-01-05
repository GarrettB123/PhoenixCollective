#--------------------------------------#
# Title: board.py
# Desc: an object that consists of everything 
# on one player's side
# Change Log: (Who, When, What)
#   Garrett Bachman, 2022-Dec-29, Created File
#   Garrett Bachman, 2022-Dec-29, Added header
#   Garrett Bachman, 2022-Dec-29, Added code
#--------------------------------------#

import random
import card
import decks

class Board:
    def __init__(self, deck):
        # lists containing data for each field in that player's side of the game
        self.library = deck.mainlist.copy()
        self.graveyard = ["none"]
        
        # split lands from battlefield else for readablility in-game
        self.battlefield = []
        self.landfield = []
        
        self.hand = []
        self.manaPool = card.Mana(0, 0, 0, 0, 0, 0, 0, 0)

    # basic funcions that help speed up game step processing
    def shuffle(self):
        random.shuffle(self.library)
    
    def draw(self, reps):
        for i in range(reps):
            self.hand.append(self.library.pop())
    
    def cast(self, index):
        if index > len(self.hand):
            print("Index out of bounds, hand size is " + len(self.hand))
        
        else: 
            self.battlefield.append(self.hand.pop(index))
            if self.battlefield[-1].type == "Land":
                self.landfield.append(self.battlefield.pop())
    
    def untap_all():
        pass
    
    def trigger():
        pass
    
    def __str__(self):
        return ("Battlefield: " + ", ".join(map(str, self.battlefield))
            + "\nLandfield: " + ", ".join(map(str, self.landfield))
            + "\nHand: " + ", ".join(map(str, self.hand))
            + "\nLibrary Size: " + str(len(self.library)))
