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
        self.is_turn = None

    # basic funcions that help speed up game step processing
    def shuffle(self):
        random.shuffle(self.library)
    
    def draw(self, reps):
        for i in range(reps):
            self.hand.append(self.library.pop())
            self.trigger("draw", self.is_turn)
    
    def cast(self, index):
        if index > len(self.hand) - 1:
            print("Index out of bounds, hand size is " + str(len(self.hand)))
        else: 
            if "Land" in self.hand[index].type:
                self.landfield.append(self.hand.pop(index))
            elif "Instant" not in self.hand[index].type and "Sorcery" not in self.hand[index].type:
                self.battlefield.append(self.hand.pop(index))
                
    
    def untap_all(self):
        for card in self.battlefield:
            card.state = "untapped"
        for card in self.landfield:
            card.state = "untapped"
    
    # for cards in the battlefield have abilities that have triggers on a certain step
    def trigger(self, event, is_my_turn):
        self.is_turn = is_my_turn
        pass
    
    def __str__(self):
        return ("Battlefield: " + ", ".join(map(str, self.battlefield))
            + "\nLandfield: " + ", ".join(map(str, self.landfield))
            + "\nHand: " + ", ".join(map(str, self.hand))
            + "\nLibrary Size: " + str(len(self.library)))
