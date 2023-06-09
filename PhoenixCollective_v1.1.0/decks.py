#--------------------------------------#
# Title: decks.py
# Desc: holds all decklists for play
# Change Log: (Who, When, What)
#   Garrett Bachman, 2023-Jan-01, Created File
#   Garrett Bachman, 2023-Jan-01, Added header
#   Garrett Bachman, 2023-Jan-01, Added code
#   Garrett Bachman, 2023-Jan-18, Fixed reference issues using deepcopy
#   Garrett Bachman, 2023-Mar-23, Changed storage datatypes from tuple to set for mutability and no duplicates
#--------------------------------------#

import copy
import database as data

class Deck:
    def __init__(self, name, size, card_list):
        self.name = name
        self.mainlist = []
        self.size = size
        for data_pair in card_list:
            for itr in range(data_pair[0]):
                self.mainlist.append(copy.deepcopy(data.dictionary[data_pair[1]]))
    def __str__(self):
        return self.name

black = Deck("black", 30, ((4, "Walking Corpse"), (4, "Barony Vampire"), (2, "Bogstomper"), (4, "Muck Rats"), (4, "Bane Alley Blackguard"), (12, "Swamp")))
red = Deck("red", 30, ((4, "Goblin Assailant"), (4, "Fearless Halberdier"), (1, "Fire Elemental"), (3, "Leopard-Spotted Jiao"), (3, "Dwarven Trader"), (12, "Mountain"), (3, "Shock")))
blue = Deck("blue", 30, ((12, "Island"), (4, "Reach Through Mists"), (3, "Merfolk of the Pearl Trident"), (3, "Fugitive Wizard"), (4, "Sworn Guardian"), (2, "Tolarian Scholar")))
red2 = Deck("red2", 30, ((9, "Goblin Assailant"), (12, "Mountain"), (9, "Shock")))
decklist = (black, red, blue, red2)