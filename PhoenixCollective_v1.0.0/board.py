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
        self.land_mana = 0
        # variable to keep track if this player lost to ensure the right player wins
        self.lost = False
        self.max_hand = 7
    
    def draw(self, reps):
        for i in range(reps):
            if len(self.library) == 0:
                self.lost = True
                break
            self.hand.append(self.library.pop())
            self.on_trigger("draw", self.is_turn)
    
    def cast(self, index):
        # checks if cast breaks casting rules
        if (len(self.hand) == 0 or index > len(self.hand) - 1 
            or (not self.is_turn and not "flash" in self.hand[index].keywords)
            or (self.lands_remaining == 0 and "Land" in self.hand[index].type)):

            print("Cannot be played currently")
            return False
        
        if "Land" in self.hand[index].type:
            self.landfield.append(self.hand.pop(index))
            self.landfield[-1].field = "battlefield"
            self.lands_remaining -= 1
            self.land_mana += 1

        else:
            # checks if theres enough mana in pool and auto taps if not
            if self.hand[index].cost.cmc() <= self.mana_pool.cmc() + self.land_mana:
                for key in self.hand[index].cost.mana.keys():
                    if self.hand[index].cost.mana[key] == 0:
                        continue
                    
                    remaining = self.hand[index].cost.mana[key] - self.mana_pool.mana[key]
                    # pre-existing mana used
                    if self.mana_pool.mana[key] >= self.hand[index].cost.mana[key]:
                        self.mana_pool.mana[key] -= self.hand[index].cost.mana[key]

                    # tap new mana
                    elif remaining != 0:
                        self.multi_tap("t" + key + str(remaining))
                        self.mana_pool.mana[key] = 0
                        if key == "n":
                            self.mana_pool.mana[self.mana_pool.max_key()] -= remaining
            else: 
                print("Not enough mana")
                return False


            if "Instant" not in self.hand[index].type and "Sorcery" not in self.hand[index].type:
                self.battlefield.append(self.hand.pop(index))
                if "Creature" in self.battlefield[-1].type:
                    self.battlefield[-1].state = "sick"
                self.battlefield[-1].field = "battlefield"
        return True
    
    def multi_tap(self, comm):
        _debt = int(comm[2:])
        _color = comm[1]
        _count = 0
        for card in self.landfield:
            # doesnt tap if the card is tapped, the wrong color, and called color isnt generic
            if card.state == "tapped" or (card.color != _color and "n" != _color):
                continue
            self.decrypt_returns(card.trigger("tap", self.is_turn))
            _count += 1
            if _count == _debt:
                break
        self.land_mana -= _count
        print("Tapped for", _count, _color)
    
    # basic funcions that help speed up game step processing
    def can_combat(self, var):
        for card in self.battlefield:
            if "Creature" in card.type and card.state == "untapped":
                return True
            if var == "blk" and "Creature" in card.type and card.state == "sick":
                return True
        return False
    
    def shuffle(self):
        random.shuffle(self.library)
      
    def heal_all(self):
        for card in self.battlefield:
            if card.type == "Creature":
                card.heal()
    
    def untap_all(self):
        self.land_mana = len(self.landfield)
        for card in self.battlefield:
            if card.state != "untapped":
                card.state = "untapped"
        for card in self.landfield:
            if card.state != "untapped":
                card.state = "untapped"
    
    # for cards in the battlefield have abilities that have triggers on a certain step
    def on_trigger(self, event, is_my_turn):
        if event != "tap" and event != "draw":
            self.mana_pool.reset()
        _perm_data = []
        self.is_turn = is_my_turn
        for perm in self.battlefield:
            _perm_data.append(perm.trigger(event, is_my_turn))
                
        for land in self.landfield:
            _perm_data.append(land.trigger(event, is_my_turn))
        if len(_perm_data) > 0 and _perm_data[0] != None:
            self.decrypt_returns(_perm_data)
    
    # processes triggers' effects on player variables
    def decrypt_returns(self, input):
        print(input)
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
            + "\nLibrary Size: " + str(len(self.library))
            + "\nGraveyard Size: " + str(len(self.graveyard))
            + "\nCMC Potential: " + str(self.mana_pool.cmc() + self.land_mana))
        if max(self.mana_pool.mana.values()) > 0:
            output += "\nMana Pool: " + str(self.mana_pool)
        return output