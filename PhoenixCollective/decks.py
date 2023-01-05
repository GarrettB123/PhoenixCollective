#--------------------------------------#
# Title: decks.py
# Desc: holds all decklists for play
# Change Log: (Who, When, What)
#   Garrett Bachman, 2023-Jan-01, Created File
#   Garrett Bachman, 2023-Jan-01, Added header
#   Garrett Bachman, 2023-Jan-01, Added code
#--------------------------------------#

import card
# TODO: add card importer cuz the manual syntax is wack asf
class Black:
    def __init__(self):
        self.mainlist = []
        self.size = 30
        self.mainlist.extend((card.Land("Swamp", "black", ("Basic",), ("Land",), ("Swamp",), "0"),) * 12)
        self.mainlist.extend((card.Creature("Walking Corpse", "black", ("",), ("Creature",), ("Zombie",), "1b", 2, 2),) * 6)
        self.mainlist.extend((card.Creature("Barony Vampire", "black", ("",), ("Creature",), ("Vampire",), "2b", 3, 2),) * 6)
        self.mainlist.extend((card.Creature("Bogstomper", "black", ("",), ("Creature",), ("Beast",), "4bb", 6, 5),) * 6)

class Red:
    def __init__(self):
        self.mainlist = []
        self.size = 30
        self.mainlist.extend((card.Land("Mountain", "red", ("Basic",), ("Land",), ("Mountian",), "0"),) * 12)
        self.mainlist.extend((card.Creature("Goblin Assailant", "red", ("",), ("Creature",), ("Goblin", "Warrior"), "1r", 2, 2),) * 6)
        self.mainlist.extend((card.Creature("Fearless Halberdier", "red", ("",), ("Creature",), ("Human", "Warrior"), "2r", 3, 2),) * 6)
        self.mainlist.extend((card.Creature("Fire Elemental", "red", ("",), ("Creature",), ("Elemental",) , "3rr", 5, 4),) * 6)
decklist = (Black(), Red())