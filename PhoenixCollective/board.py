#--------------------------------------#
# Title: board.py
# Desc: an object that consists of everything 
# on one player's side
# Change Log: (Who, When, What)
#   Garrett Bachman, 2022-Dec-29, Created File
#   Garrett Bachman, 2022-Dec-29, Added header
#   Garrett Bachman, 2022-Dec-29, Added code
#--------------------------------------#

import card
import main
import random
import copy

class Board:
    def __init__(self, deck):
        # lists containing data for each field in that player's side of the game
        self.library = copy.deepcopy(deck.mainlist)
        self.graveyard = []
        # split lands from battlefield else for readablility in-game
        self.battlefield = []
        self.landfield = []
        self.hand = []
        self.mana_pool = card.Mana(0, 0, 0, 0, 0, 0, 0, 0)
        
        self.is_turn = None
        self.life_total = 0
        self.lands_remaining = 0
        # variable to keep track if this player lost to ensure the right player wins
        self.lost = False
    # basic funcions that help speed up game step processing
    def shuffle(self):
        random.shuffle(self.library)
    
    def draw(self, reps):
        for i in range(reps):
            if len(self.library) == 0:
                self.lost = True
            self.hand.append(self.library.pop())
            self.on_trigger("draw", self.is_turn)
    
    def cast(self, index):
        if ((not self.is_turn and not "flash" in self.hand[index].keywords)
            or (self.lands_remaining == 0 and "Land" in self.hand[index].type)):
            print("Cannot be played")
            return False
        #if self.hand[index].cost > self.mana_pool:
        #    pass
        if "Land" in self.hand[index].type:
            self.landfield.append(self.hand.pop(index))
            self.landfield[-1].field = "battlefield"
        elif "Instant" not in self.hand[index].type and "Sorcery" not in self.hand[index].type:
            self.battlefield.append(self.hand.pop(index))
            if "Creature" in self.battlefield[-1].type:
                self.battlefield[-1].state = "sick"
            self.battlefield[-1].field = "battlefield"
        return True
                
    def heal_all(self):
        for card in self.battlefield:
            if card.type == "Creature":
                card.heal()
    
    def untap_all(self):
        for card in self.battlefield:
            if card.state != "untapped":
                card.state = "untapped"
        for card in self.landfield:
            if card.state != "untapped":
                card.state = "untapped"
    
    # for cards in the battlefield have abilities that have triggers on a certain step
    def on_trigger(self, event, is_my_turn):
        _perm_data = []
        self.is_turn = is_my_turn
        for perm in self.battlefield:
            _perm_data.append(perm.trigger(event, is_my_turn))
                
        for land in self.landfield:
            _perm_data.append(_land_data = land.trigger(event, is_my_turn))
        
    def decrypt_returns(self, input):
        if type(input[0]) == str:
            input = (input,)
        
        for in_list in input:
            target = in_list[0]
            in_list = in_list[1:]
            for command in in_list:
                if target == "mana":
                    self.mana_pool.mana[command[0]] += command[1]
                    
                    
            
    def __str__(self):
        output = ("Life total: " + str(self.life_total)
            + "\nBattlefield: " + ", ".join(map(str, self.battlefield))
            + "\nLandfield: " + ", ".join(map(str, self.landfield))
            + "\nHand: " + ", ".join(map(str, self.hand))
            + "\nLibrary Size: " + str(len(self.library)))
        if max(self.mana_pool.mana.values()) > 0:
            output += "\nMana Pool: " + str(self.mana_pool)
        return output