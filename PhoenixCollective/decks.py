#--------------------------------------#
# Title: decks.py
# Desc: holds all decklists for play
# Change Log: (Who, When, What)
#   Garrett Bachman, 2023-Jan-01, Created File
#   Garrett Bachman, 2023-Jan-01, Added header
#   Garrett Bachman, 2023-Jan-01, Added code
#   Garrett Bachman, 2023-Jan-18, Fixed reference issues using deepcopy
#--------------------------------------#

import card
import copy

# TODO: add card importer much later
class Black:
    def __init__(self):
        self.mainlist = []
        self.size = 30
        for i in range(self.size):
            if i <= 6:
                self.mainlist.append(copy.deepcopy(Database.WALKING_CORPSE))
                self.mainlist.append(copy.deepcopy(Database.BARONY_VAMPIRE))
                self.mainlist.append(copy.deepcopy(Database.BOGSTOMPER))
            if i <= 12:
                self.mainlist.append(copy.deepcopy(Database.SWAMP))

class Red:
    def __init__(self):
        self.mainlist = []
        self.size = 30
        while len(self.mainlist) <= self.size:
            if len(self.mainlist) <= 18:
                self.mainlist.append(copy.deepcopy(Database.GOBLIN_ASSAILANT))
                self.mainlist.append(copy.deepcopy(Database.FEARLESS_HALPERDIER))
                self.mainlist.append(copy.deepcopy(Database.FIRE_ELEMENTAL))
            else:
                self.mainlist.append(copy.deepcopy(Database.MOUNTAIN))

class Database:
    SWAMP = card.Land("Swamp", "b", ("Basic",), ("Land",), ("Swamp",), "0", (None,))
    WALKING_CORPSE = card.Creature("Walking Corpse", "b", ("",), ("Creature",), ("Zombie",), "1b", (None,), 2, 2)
    BARONY_VAMPIRE = card.Creature("Barony Vampire", "b", ("",), ("Creature",), ("Vampire",), "2b", (None,), 3, 2)
    BOGSTOMPER = card.Creature("Bogstomper", "b", ("",), ("Creature",), ("Beast",), "4bb", (None,), 6, 5)
    MOUNTAIN = card.Land("Mountain", "r", ("Basic",), ("Land",), ("Mountian",), "0", (None,))
    GOBLIN_ASSAILANT = card.Creature("Goblin Assailant", "r", ("",), ("Creature",), ("Goblin", "Warrior"), "1r", (None,), 2, 2)
    FEARLESS_HALPERDIER = card.Creature("Fearless Halberdier", "r", ("",), ("Creature",), ("Human", "Warrior"), "2r", (None,), 3, 2)
    FIRE_ELEMENTAL = card.Creature("Fire Elemental", "r", ("",), ("Creature",), ("Elemental",) , "3rr", (None,), 5, 4)

decklist = (Black(), Red())